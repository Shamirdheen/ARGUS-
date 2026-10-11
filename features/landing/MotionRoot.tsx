"use client";

import { useEffect } from "react";
import "./motion.css";

/**
 * One IntersectionObserver for the whole landing page: any element with `data-reveal`
 * gets `data-in` the first time it scrolls into view. CSS in motion.css does the rest.
 * Server components only need the attribute — no client wrapper per section.
 */
export function MotionRoot() {
  useEffect(() => {
    const els = Array.from(document.querySelectorAll<HTMLElement>("[data-reveal]"));
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced || !("IntersectionObserver" in window)) {
      els.forEach((el) => el.setAttribute("data-in", ""));
      return;
    }
    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (!e.isIntersecting) continue;
          e.target.setAttribute("data-in", "");
          io.unobserve(e.target);
        }
      },
      { rootMargin: "0px 0px -12% 0px", threshold: 0.12 },
    );
    els.forEach((el) => io.observe(el));
    return () => io.disconnect();
  }, []);
  return null;
}

/** Fires once when the element first enters the viewport (used by the count-up and auto-demo). */
export function useInViewOnce<T extends HTMLElement>(ref: React.RefObject<T | null>, onEnter: () => void) {
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (!("IntersectionObserver" in window)) return onEnter();
    const io = new IntersectionObserver(
      ([e]) => {
        if (e.isIntersecting) {
          onEnter();
          io.disconnect();
        }
      },
      { threshold: 0.4 },
    );
    io.observe(el);
    return () => io.disconnect();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ref]);
}

export const prefersReducedMotion = () =>
  typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

/** Animate a number from `from` to `to` over `ms` with the Argus ease-out. */
export function tween(from: number, to: number, ms: number, onFrame: (v: number) => void) {
  if (prefersReducedMotion()) return onFrame(to);
  const start = performance.now();
  const ease = (t: number) => 1 - Math.pow(1 - t, 3);
  let raf = 0;
  const step = (now: number) => {
    const t = Math.min(1, (now - start) / ms);
    onFrame(from + (to - from) * ease(t));
    if (t < 1) raf = requestAnimationFrame(step);
  };
  raf = requestAnimationFrame(step);
  return () => cancelAnimationFrame(raf);
}
