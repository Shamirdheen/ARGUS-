import type { Risk } from "@/lib/positions/types";

const OPEN: Record<Risk, number> = { safe: 0.32, watch: 0.55, warning: 0.78, critical: 1 };
const IRIS: Record<Risk, number> = { safe: 0.6, watch: 0.8, warning: 0.95, critical: 1.05 };
const LID: Record<Risk, string> = { safe: "#7e654a", watch: "#efc796", warning: "#e0946a", critical: "#e0946a" };
const FILL: Record<Risk, string> = { safe: "none", watch: "none", warning: "#c0551e", critical: "#e0946a" };
const INK = "#16110c";

/**
 * The risk eye: the lid opens and the iris brightens as health falls.
 * `onFill` draws it in ink, for use on the terracotta critical row.
 */
export function RiskEye({
  risk,
  size = 22,
  onFill = false,
  glow = false,
  className,
}: {
  risk: Risk;
  size?: number;
  onFill?: boolean;
  glow?: boolean;
  className?: string;
}) {
  const lid = onFill ? INK : LID[risk];
  const iris = onFill ? INK : FILL[risk];
  return (
    <svg
      viewBox="0 0 400 240"
      width={size}
      height={Math.round(size * 0.6)}
      aria-hidden="true"
      className={className}
      style={{ flex: "none", overflow: "visible" }}
    >
      {glow && risk === "critical" && (
        <ellipse className="risk-eye-glow" cx="200" cy="120" rx="170" ry="90" fill="#c0551e" opacity=".45" style={{ filter: "blur(22px)" }} />
      )}
      <g className="risk-eye-lid" style={{ transform: `scaleY(${OPEN[risk]})` }}>
        <path
          d="M20 120 Q200 -10 380 120 Q200 250 20 120Z"
          fill={size > 40 ? INK : "none"}
          stroke={lid}
          strokeWidth={2.4}
          vectorEffect="non-scaling-stroke"
        />
      </g>
      <circle
        className="risk-eye-iris"
        cx="200"
        cy="120"
        r="64"
        fill={iris}
        stroke={lid}
        strokeWidth={2}
        vectorEffect="non-scaling-stroke"
        style={{ transform: `scale(${IRIS[risk]})` }}
      />
    </svg>
  );
}

/** Small "Argus is opening his eyes…" loader. */
export function OpeningEye({ label = "Argus is opening his eyes…" }: { label?: string }) {
  return (
    <span role="status" className="inline-flex items-center gap-2.5 text-[13px] text-sand-500">
      <svg viewBox="0 0 400 240" width="30" height="18" aria-hidden="true">
        <g className="argus-opening">
          <path d="M20 120 Q200 -10 380 120 Q200 250 20 120Z" fill="none" stroke="#efc796" strokeWidth={3} vectorEffect="non-scaling-stroke" />
        </g>
      </svg>
      {label}
    </span>
  );
}
