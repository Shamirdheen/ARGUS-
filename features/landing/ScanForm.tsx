"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

const BASE58 = /^[1-9A-HJ-NP-Za-km-z]{32,44}$/;

export function ScanForm() {
  const router = useRouter();
  const [value, setValue] = useState("");
  const [error, setError] = useState<string | null>(null);

  return (
    <form
      className="flex flex-col gap-2"
      onSubmit={(e) => {
        e.preventDefault();
        const v = value.trim();
        if (!v) return router.push("/app");
        if (!BASE58.test(v)) return setError("That doesn't look like a Solana address.");
        router.push(`/app?wallet=${v}`);
      }}
    >
      <div className="flex gap-2 flex-wrap">
        <label htmlFor="wallet" className="sr-only">
          Solana wallet address
        </label>
        <input
          id="wallet"
          type="text"
          value={value}
          onChange={(e) => {
            setValue(e.target.value);
            setError(null);
          }}
          placeholder="Wallet address"
          autoComplete="off"
          spellCheck={false}
          className="flex-[1_1_240px] min-w-0 min-h-11 px-3.5 bg-ink-900 border border-ink-700 text-sm text-sand-100 placeholder:text-sand-600 focus:outline-none focus:border-sand-500"
        />
        <button type="submit" className="min-h-11 px-5 bg-sand-200 text-ink-950 text-sm font-medium hover:bg-sand-100 cursor-pointer">
          Scan wallet →
        </button>
      </div>
      {error ? (
        <span className="text-[12px] text-risk-warning">{error}</span>
      ) : (
        <span className="text-[12px] text-sand-500">Read-only. No signature, no keys. Leave it empty to see the demo book.</span>
      )}
    </form>
  );
}
