"use client";

import { useState, type ReactNode } from "react";
import { cx } from "./index";

/**
 * Marks a value that just changed: when `value` differs from the last render, the content
 * re-mounts with the `.tick` class (a one-off glow from app-motion.css). Never on first render,
 * so loading a page doesn't flash every number — only real updates (30s refresh, new data) do.
 */
export function Ticker({ value, children, className }: { value: string | number; children: ReactNode; className?: string }) {
  // Adjust state during render when the prop changes (React's documented pattern; no effect needed).
  const [seen, setSeen] = useState({ value, n: 0 });
  if (seen.value !== value) setSeen({ value, n: seen.n + 1 });
  return (
    <span key={seen.n} className={cx(seen.n > 0 && "tick", className)}>
      {children}
    </span>
  );
}
