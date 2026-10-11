import Anthropic from "@anthropic-ai/sdk";
import { systemPrompt } from "@/features/ask/prompt";
import type { AskAction, AskEvent, ChatTurn } from "@/features/ask/types";
import { hfAfterMove } from "@/lib/positions/risk";
import type { PortfolioSnapshot } from "@/lib/positions/types";

const MODEL = process.env.ARGUS_MODEL || "claude-sonnet-5-5";
const MAX_TOOL_ROUNDS = 3;

const TOOLS: Anthropic.Tool[] = [
  {
    name: "simulate_price_move",
    description:
      "Health factor of each position after its collateral price moves by a percentage (borrow assumed stable). Use for any move not in the pre-computed shocks.",
    input_schema: {
      type: "object",
      properties: {
        move_pct: { type: "number", description: "Percent change, e.g. -30 for a 30% drop." },
        position_ids: { type: "array", items: { type: "string" }, description: "Optional subset; default all." },
      },
      required: ["move_pct"],
    },
  },
  {
    name: "suggest_action",
    description: "Show the user a one-tap next step in the app. Argus never executes it; the user does.",
    input_schema: {
      type: "object",
      properties: {
        kind: { type: "string", enum: ["add_collateral", "repay", "open_position", "rehearse_move"] },
        position_id: { type: "string" },
        amount_usd: { type: "number", description: "For add_collateral / repay." },
        move_pct: { type: "number", description: "For rehearse_move." },
        reason: { type: "string", description: "One short line, shown under the button." },
      },
      required: ["kind", "reason"],
    },
  },
];

export async function POST(request: Request) {
  if (!process.env.ANTHROPIC_API_KEY) {
    return Response.json({ error: "Ask Argus isn't configured: set ANTHROPIC_API_KEY on the server." }, { status: 503 });
  }

  let body: { messages: ChatTurn[]; snapshot: PortfolioSnapshot };
  try {
    body = await request.json();
  } catch {
    return Response.json({ error: "Bad request" }, { status: 400 });
  }
  const turns = (body.messages ?? []).slice(-20).filter((m) => m.content?.trim());
  const snapshot = body.snapshot;
  if (!turns.length || !snapshot?.positions) return Response.json({ error: "Bad request" }, { status: 400 });

  const client = new Anthropic();
  const messages: Anthropic.MessageParam[] = turns.map((t) => ({ role: t.role, content: t.content.slice(0, 4000) }));
  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    async start(controller) {
      const send = (e: AskEvent) => controller.enqueue(encoder.encode(JSON.stringify(e) + "\n"));
      try {
        for (let round = 0; round <= MAX_TOOL_ROUNDS; round++) {
          const s = client.messages.stream(
            { model: MODEL, max_tokens: 1024, system: systemPrompt(snapshot), tools: TOOLS, messages },
            { signal: request.signal },
          );
          s.on("text", (delta) => send({ type: "text", text: delta }));
          const msg = await s.finalMessage();
          messages.push({ role: "assistant", content: msg.content });
          if (msg.stop_reason !== "tool_use") break;

          const results: Anthropic.ToolResultBlockParam[] = [];
          for (const block of msg.content) {
            if (block.type !== "tool_use") continue;
            const input = block.input as Record<string, unknown>;
            if (block.name === "simulate_price_move") {
              const move = Number(input.move_pct) / 100;
              const ids = Array.isArray(input.position_ids) ? (input.position_ids as string[]) : null;
              const out = snapshot.positions
                .filter((p) => !ids || ids.includes(p.id))
                .map((p) => {
                  const hf = hfAfterMove(p, move);
                  return { id: p.id, name: p.name, health_before: +p.healthFactor.toFixed(2), health_after: +hf.toFixed(2), liquidated: hf < 1 };
                });
              results.push({ type: "tool_result", tool_use_id: block.id, content: JSON.stringify(out) });
            } else if (block.name === "suggest_action") {
              send({ type: "action", action: input as unknown as AskAction });
              results.push({ type: "tool_result", tool_use_id: block.id, content: "Shown to the user as a button." });
            } else {
              results.push({ type: "tool_result", tool_use_id: block.id, content: "Unknown tool", is_error: true });
            }
          }
          messages.push({ role: "user", content: results });
          send({ type: "text", text: "\n\n" });
        }
        send({ type: "done" });
      } catch (err) {
        const message = err instanceof Anthropic.APIError ? `Claude API error (${err.status ?? "network"})` : "Argus lost sight for a moment. Try again.";
        send({ type: "error", message });
      } finally {
        controller.close();
      }
    },
  });

  return new Response(stream, {
    headers: { "content-type": "application/x-ndjson; charset=utf-8", "cache-control": "no-store" },
  });
}
