export interface ChatTurn {
  role: "user" | "assistant";
  content: string;
}

export interface AskAction {
  kind: "add_collateral" | "repay" | "open_position" | "rehearse_move";
  position_id?: string;
  amount_usd?: number;
  move_pct?: number;
  reason: string;
}

export type AskEvent =
  | { type: "text"; text: string }
  | { type: "action"; action: AskAction }
  | { type: "error"; message: string }
  | { type: "done" };
