"use client";

import { useCallback, useState } from "react";

/**
 * Lets a panel play its exit animation before it unmounts.
 * `close()` flips `leaving` (so the panel can swap to `.panel-out` / `.backdrop-out`),
 * then calls `onDone` after `ms`. With reduced motion it closes immediately.
 */
export function useExit(onDone: () => void, ms = 220) {
  const [leaving, setLeaving] = useState(false);
  const close = useCallback(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return onDone();
    setLeaving(true);
    window.setTimeout(() => {
      setLeaving(false);
      onDone();
    }, ms);
  }, [onDone, ms]);
  return { leaving, close };
}
