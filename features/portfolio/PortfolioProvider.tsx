"use client";

import { useWallet } from "@solana/wallet-adapter-react";
import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from "react";
import type { PortfolioSnapshot } from "@/lib/positions/types";

interface Ctx {
  snapshot: PortfolioSnapshot | null;
  loading: boolean;
  refresh: () => void;
  selectedId: string | null;
  select: (id: string | null) => void;
  askOpen: boolean;
  setAskOpen: (v: boolean) => void;
  askSeed: string | null;
  ask: (q: string) => void;
  clearSeed: () => void;
}

const PortfolioContext = createContext<Ctx | null>(null);
const REFRESH_MS = 30_000;

export function PortfolioProvider({ children }: { children: ReactNode }) {
  const { publicKey } = useWallet();
  // A pasted address (?wallet=…) is watched read-only; a connected wallet takes priority.
  const [watched] = useState<string | null>(() =>
    typeof window === "undefined" ? null : new URLSearchParams(window.location.search).get("wallet"),
  );
  const wallet = publicKey?.toBase58() ?? watched;
  const [snapshot, setSnapshot] = useState<PortfolioSnapshot | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedId, select] = useState<string | null>(null);
  const [askOpen, setAskOpen] = useState(false);
  const [askSeed, setAskSeed] = useState<string | null>(null);
  const [tick, setTick] = useState(0);

  useEffect(() => {
    const ctrl = new AbortController();
    fetch(`/api/positions${wallet ? `?wallet=${wallet}` : ""}`, { signal: ctrl.signal, cache: "no-store" })
      .then((r) => r.json() as Promise<PortfolioSnapshot>)
      .then((s) => setSnapshot(s))
      .catch(() => {})
      .finally(() => setLoading(false));
    return () => ctrl.abort();
  }, [wallet, tick]);

  useEffect(() => {
    const id = setInterval(() => setTick((t) => t + 1), REFRESH_MS);
    return () => clearInterval(id);
  }, []);

  // ⌘K / Ctrl+K opens Ask Argus anywhere in the app.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setAskOpen(true);
      }
      if (e.key === "Escape") setAskOpen(false);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  const refresh = useCallback(() => setTick((t) => t + 1), []);
  const ask = useCallback((q: string) => {
    setAskSeed(q);
    setAskOpen(true);
  }, []);

  return (
    <PortfolioContext.Provider
      value={{ snapshot, loading, refresh, selectedId, select, askOpen, setAskOpen, askSeed, ask, clearSeed: () => setAskSeed(null) }}
    >
      {children}
    </PortfolioContext.Provider>
  );
}

export function usePortfolio() {
  const c = useContext(PortfolioContext);
  if (!c) throw new Error("usePortfolio must be used inside <PortfolioProvider>");
  return c;
}
