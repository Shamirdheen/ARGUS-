"use client";

import { ArrowUp, X } from "@phosphor-icons/react";
import { useCallback, useEffect, useRef, useState } from "react";
import { OpeningEye } from "@/components/brand/RiskEye";
import { Button } from "@/components/ui";
import { usePortfolio } from "@/features/portfolio/PortfolioProvider";
import { useExit } from "@/features/shell/useExit";
import { usd } from "@/lib/positions/risk";
import { PROTOCOL_APP_URL } from "@/lib/positions/types";
import type { AskAction, AskEvent, ChatTurn } from "./types";

interface Msg extends ChatTurn {
  actions?: AskAction[];
  error?: boolean;
}

const STARTERS = [
  "Am I safe?",
  "Which position breaks first if SOL drops 25%?",
  "How do I protect my riskiest position?",
  "What happens if I get liquidated?",
  "Explain health factor",
];

function Markdownish({ text, caret = false }: { text: string; caret?: boolean }) {
  // Bold (**x**) and line breaks only — enough for Argus's short answers, no HTML injection.
  const paras = text.trim().split(/\n{2,}/);
  return (
    <>
      {paras.map((para, i) => (
          <p key={i} className={`m-0 whitespace-pre-wrap ${caret && i === paras.length - 1 ? "caret" : ""}`}>
            {para.split(/(\*\*[^*]+\*\*)/g).map((seg, j) =>
              seg.startsWith("**") && seg.endsWith("**") ? (
                <b key={j} className="font-medium text-sand-100">
                  {seg.slice(2, -2)}
                </b>
              ) : (
                seg
              ),
            )}
          </p>
        ))}
    </>
  );
}

export function AskPanel() {
  const { askOpen, setAskOpen, askSeed, clearSeed, snapshot, select } = usePortfolio();
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const scroller = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const abort = useRef<AbortController | null>(null);

  useEffect(() => {
    if (askOpen) setTimeout(() => inputRef.current?.focus(), 50);
  }, [askOpen]);

  const { leaving, close } = useExit(useCallback(() => setAskOpen(false), [setAskOpen]));
  useEffect(() => {
    if (!askOpen) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && close();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [askOpen, close]);

  useEffect(() => {
    scroller.current?.scrollTo({ top: scroller.current.scrollHeight });
  }, [messages]);

  async function send(text: string) {
    const q = text.trim();
    if (!q || busy || !snapshot) return;
    const history: Msg[] = [...messages, { role: "user", content: q }];
    setMessages([...history, { role: "assistant", content: "" }]);
    setInput("");
    setBusy(true);
    abort.current = new AbortController();

    const patch = (fn: (m: Msg) => Msg) =>
      setMessages((ms) => {
        const copy = ms.slice();
        copy[copy.length - 1] = fn(copy[copy.length - 1]);
        return copy;
      });

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          messages: history.filter((m) => !m.error).map(({ role, content }) => ({ role, content })),
          snapshot,
        }),
        signal: abort.current.signal,
      });
      if (!res.ok || !res.body) {
        const err = await res.json().catch(() => ({ error: "Argus couldn't answer." }));
        patch((m) => ({ ...m, content: err.error ?? "Argus couldn't answer.", error: true }));
        return;
      }
      const reader = res.body.getReader();
      const dec = new TextDecoder();
      let buf = "";
      for (;;) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });
        const lines = buf.split("\n");
        buf = lines.pop() ?? "";
        for (const line of lines) {
          if (!line.trim()) continue;
          const e = JSON.parse(line) as AskEvent;
          if (e.type === "text") patch((m) => ({ ...m, content: m.content + e.text }));
          else if (e.type === "action") patch((m) => ({ ...m, actions: [...(m.actions ?? []), e.action] }));
          else if (e.type === "error") patch((m) => ({ ...m, content: (m.content ? m.content + "\n\n" : "") + e.message, error: true }));
        }
      }
    } catch (err) {
      if ((err as Error).name !== "AbortError") patch((m) => ({ ...m, content: "Argus lost sight for a moment. Try again.", error: true }));
    } finally {
      setBusy(false);
    }
  }

  // Questions asked from elsewhere in the app ("Ask Argus about this").
  useEffect(() => {
    if (askOpen && askSeed && snapshot && !busy) {
      clearSeed();
      // eslint-disable-next-line react-hooks/set-state-in-effect -- a question handed over from elsewhere in the app
      void send(askSeed);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [askOpen, askSeed, snapshot]);

  function actionButton(a: AskAction, key: number) {
    const p = snapshot?.positions.find((x) => x.id === a.position_id);
    const label =
      a.kind === "add_collateral"
        ? `Add ${a.amount_usd ? usd(a.amount_usd) : "collateral"}${p ? ` to ${p.name}` : ""}`
        : a.kind === "repay"
          ? `Repay ${a.amount_usd ? usd(a.amount_usd) : "debt"}${p ? ` on ${p.name}` : ""}`
          : a.kind === "rehearse_move"
            ? `Rehearse ${a.move_pct ?? ""}%`
            : `Open ${p?.name ?? "position"}`;
    return (
      <div key={key} className="msg-in flex flex-col gap-1.5 p-3 border border-dashed border-sand-600">
        <div className="flex items-center justify-between gap-3">
          <span className="text-[13px] text-sand-100 font-medium">{label}</span>
          {p && (
            <div className="flex items-center gap-2 shrink-0">
              <Button
                kind="secondary"
                small
                onClick={() => {
                  setAskOpen(false);
                  select(p.id);
                }}
              >
                {a.kind === "add_collateral" || a.kind === "repay" ? "Details" : "Open"}
              </Button>
              {(a.kind === "add_collateral" || a.kind === "repay") && (
                <Button kind="primary" small onClick={() => window.open(PROTOCOL_APP_URL[p.protocol], "_blank", "noopener,noreferrer")}>
                  Open on {p.protocol} ↗
                </Button>
              )}
            </div>
          )}
        </div>
        <span className="text-[12px] text-sand-500">{a.reason}</span>
      </div>
    );
  }

  if (!askOpen) return null;
  const streamingIndex = busy ? messages.length - 1 : -1;

  return (
    <div className="fixed inset-0 z-50" role="dialog" aria-modal="true" aria-label="Ask Argus">
      <button
        type="button"
        aria-label="Close Ask Argus"
        className={`${leaving ? "backdrop-out" : "backdrop-in"} absolute inset-0 bg-ink-950/70 cursor-default`}
        onClick={close}
      />
      <aside className={`${leaving ? "panel-out" : "panel-in"} absolute top-0 right-0 bottom-0 w-full max-w-[520px] bg-ink-900 border-l border-ink-700 flex flex-col`}>
        <div className="flex items-center justify-between gap-3 px-5 py-4 border-b border-ink-800">
          <div className="flex flex-col gap-1">
            <span className="font-display text-[18px] text-sand-100">Ask Argus</span>
            <span className="text-[12px] text-sand-500">
              Reads your {snapshot?.positions.length ?? 0} positions · read-only · not financial advice
            </span>
          </div>
          <button type="button" onClick={close} aria-label="Close" className="min-w-10 min-h-10 grid place-items-center border border-ink-700 text-sand-200 cursor-pointer hover:bg-ink-850">
            <X size={18} weight="light" />
          </button>
        </div>

        <div ref={scroller} className="flex-1 overflow-y-auto px-5 py-5 flex flex-col gap-5" aria-live="polite">
          {messages.length === 0 && (
            <div className="flex flex-col gap-3">
              <p className="m-0 text-sm text-sand-300 leading-relaxed">
                I&apos;m watching every position. Ask what&apos;s at risk, what a price move would do, or how to get back to safe.
              </p>
            </div>
          )}
          {messages.map((m, i) =>
            m.role === "user" ? (
              <div key={i} className="msg-in self-end max-w-[85%] bg-ink-850 border border-ink-700 px-3.5 py-3 text-sm leading-relaxed text-sand-100">
                {m.content}
              </div>
            ) : (
              <div key={i} className="msg-in flex gap-3 items-start">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src="/brand/argus-mark-S-dark.svg" alt="" width={26} height={26} className="mt-0.5 shrink-0" />
                <div className={`flex-1 min-w-0 flex flex-col gap-3 text-sm leading-relaxed ${m.error ? "text-risk-warning" : "text-sand-300"}`}>
                  {m.content ? <Markdownish text={m.content} caret={i === streamingIndex} /> : busy && i === messages.length - 1 ? <OpeningEye label="Argus is looking…" /> : null}
                  {m.actions?.map(actionButton)}
                </div>
              </div>
            ),
          )}
        </div>

        <div className="border-t border-ink-800 px-5 py-4 flex flex-col gap-2.5">
          {messages.length === 0 && (
            <div className="flex gap-2 flex-wrap">
              {STARTERS.map((s) => (
                <button key={s} type="button" onClick={() => send(s)} className="min-h-9 px-3 border border-ink-700 text-[12px] text-sand-300 hover:bg-ink-850 cursor-pointer">
                  {s}
                </button>
              ))}
            </div>
          )}
          <form
            className="flex gap-2"
            onSubmit={(e) => {
              e.preventDefault();
              void send(input);
            }}
          >
            <label htmlFor="ask-input" className="sr-only">
              Ask about your positions
            </label>
            <textarea
              id="ask-input"
              ref={inputRef}
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  void send(input);
                }
              }}
              placeholder="Ask about your positions…"
              className="flex-1 min-w-0 min-h-11 max-h-32 resize-none px-3 py-2.5 bg-ink-950 border border-ink-700 text-sm text-sand-100 placeholder:text-sand-600 focus:outline-none focus:border-sand-500"
            />
            {busy ? (
              <Button kind="secondary" onClick={() => abort.current?.abort()}>
                Stop
              </Button>
            ) : (
              <Button type="submit" aria-label="Ask" disabled={!input.trim()}>
                <ArrowUp size={16} weight="light" />
              </Button>
            )}
          </form>
        </div>
      </aside>
    </div>
  );
}
