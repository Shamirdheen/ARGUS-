import type { ButtonHTMLAttributes, ReactNode } from "react";
import { RiskEye } from "@/components/brand/RiskEye";
import { hfText, riskLabel, riskOf } from "@/lib/positions/risk";
import type { Risk } from "@/lib/positions/types";

export function cx(...c: (string | false | null | undefined)[]) {
  return c.filter(Boolean).join(" ");
}

type Kind = "primary" | "secondary" | "simulate" | "danger" | "ghost";
const KIND: Record<Kind, string> = {
  primary: "bg-sand-200 text-ink-950 border border-sand-200 hover:bg-sand-100",
  secondary: "bg-transparent text-sand-200 border border-ink-700 hover:bg-ink-850",
  simulate: "bg-transparent text-sand-200 border border-dashed border-sand-600 hover:bg-ink-850",
  danger: "bg-risk-critical text-ink-950 border border-risk-critical hover:bg-terra-300",
  ghost: "bg-transparent text-sand-300 border border-transparent hover:text-sand-100",
};

export function Button({
  kind = "primary",
  small,
  className,
  ...rest
}: ButtonHTMLAttributes<HTMLButtonElement> & { kind?: Kind; small?: boolean }) {
  return (
    <button
      type="button"
      {...rest}
      className={cx(
        "inline-flex items-center justify-center gap-2 font-medium transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed",
        small ? "min-h-9 px-3.5 text-[13px]" : "min-h-11 px-[18px] text-sm",
        KIND[kind],
        className,
      )}
    />
  );
}

export function Label({ children, className }: { children: ReactNode; className?: string }) {
  return <span className={cx("text-[11px] font-medium uppercase tracking-[0.1em] text-sand-500", className)}>{children}</span>;
}

export function Card({ children, className }: { children: ReactNode; className?: string }) {
  return <div className={cx("bg-ink-900 border border-ink-800 p-[22px] flex flex-col gap-3.5 min-w-0", className)}>{children}</div>;
}

export function H1({ children }: { children: ReactNode }) {
  return <h1 className="font-display text-[28px] md:text-[34px] leading-[1.1] text-sand-100 m-0">{children}</h1>;
}
export function H2({ children }: { children: ReactNode }) {
  return <h2 className="font-display text-[15px] md:text-[17px] leading-[1.2] tracking-[0.06em] uppercase text-sand-100 m-0">{children}</h2>;
}

const HF_COLOR: Record<Risk, string> = {
  safe: "text-risk-safe",
  watch: "text-risk-watch",
  warning: "text-risk-warning underline decoration-2 underline-offset-4",
  critical: "text-risk-critical",
};

export function Health({ value, onFill, className }: { value: number; onFill?: boolean; className?: string }) {
  const r = riskOf(value);
  return <span className={cx("font-medium tabular-nums", onFill ? "text-ink-950" : HF_COLOR[r], className)}>{hfText(value)}</span>;
}

export function Status({ risk, onFill }: { risk: Risk; onFill?: boolean }) {
  return (
    <span className="inline-flex items-center gap-2">
      <RiskEye risk={risk} onFill={onFill} />
      {risk === "critical" ? (
        <span className="text-[12px] font-medium leading-none px-2 py-1.5 bg-ink-950 text-risk-critical">{riskLabel(risk)}</span>
      ) : risk === "warning" ? (
        <span className="text-[13px] font-medium text-risk-warning">{riskLabel(risk)}</span>
      ) : risk === "watch" ? (
        <span className="text-[13px] text-sand-200">{riskLabel(risk)}</span>
      ) : (
        <span className="sr-only">{riskLabel(risk)}</span>
      )}
    </span>
  );
}

export function Stat({ label, value, sub }: { label: string; value: ReactNode; sub?: ReactNode }) {
  return (
    <div className="flex flex-col gap-1.5 min-w-0">
      <Label>{label}</Label>
      <span className="text-[22px] font-medium text-sand-100 tabular-nums truncate">{value}</span>
      {sub && <span className="text-[12px] text-sand-500">{sub}</span>}
    </div>
  );
}
