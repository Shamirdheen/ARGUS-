"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { MagnifyingGlass } from "@phosphor-icons/react";
import type { ReactNode } from "react";
import { cx } from "@/components/ui";
import { usePortfolio } from "@/features/portfolio/PortfolioProvider";
import { WalletButton } from "@/features/wallet/WalletButton";
import { AskPanel } from "@/features/ask/AskPanel";
import { PositionDrawer } from "@/features/positions/PositionDrawer";

const NAV = [
  { href: "/app", label: "Overview" },
  { href: "/app/positions", label: "Positions" },
] as const;

export function AppShell({ children }: { children: ReactNode }) {
  const path = usePathname();
  const { snapshot, setAskOpen } = usePortfolio();

  return (
    <div className="min-h-dvh flex flex-col">
      <header className="sticky top-0 z-30 bg-ink-950/95 backdrop-blur border-b border-ink-800">
        <div className="mx-auto max-w-[1280px] px-4 md:px-8 h-16 flex items-center gap-6">
          <Link href="/" className="shrink-0" aria-label="Argus home">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src="/brand/argus-lockup-dark.svg" alt="Argus" width={105} height={30} className="h-[30px] w-auto" />
          </Link>
          <nav className="hidden sm:flex items-center gap-1" aria-label="Main">
            {NAV.map((n) => {
              const active = n.href === "/app" ? path === "/app" : path.startsWith(n.href);
              return (
                <Link
                  key={n.href}
                  href={n.href}
                  aria-current={active ? "page" : undefined}
                  className={cx(
                    "px-3 py-2 text-[13px] transition-colors",
                    active ? "text-sand-100 shadow-[inset_0_-2px_0_var(--color-sand-200)]" : "text-sand-500 hover:text-sand-200",
                  )}
                >
                  {n.label}
                </Link>
              );
            })}
          </nav>
          <div className="ml-auto flex items-center gap-2">
            {snapshot?.source === "demo" && (
              <span className="hidden md:inline text-[11px] uppercase tracking-[0.1em] text-sand-500 border border-ink-700 px-2 py-1">Demo data</span>
            )}
            <button
              type="button"
              onClick={() => setAskOpen(true)}
              className="hidden md:inline-flex items-center gap-2 min-h-9 px-3 border border-ink-700 text-[13px] text-sand-300 hover:bg-ink-850 cursor-pointer"
            >
              <MagnifyingGlass size={16} weight="light" aria-hidden />
              Ask Argus
              <kbd className="text-[11px] text-sand-500 border border-ink-700 px-1.5 py-px">⌘K</kbd>
            </button>
            <WalletButton />
          </div>
        </div>
        <nav className="sm:hidden flex border-t border-ink-800" aria-label="Main mobile">
          {NAV.map((n) => (
            <Link key={n.href} href={n.href} className={cx("flex-1 text-center py-2.5 text-[13px]", path === n.href ? "text-sand-100" : "text-sand-500")}>
              {n.label}
            </Link>
          ))}
          <button type="button" onClick={() => setAskOpen(true)} className="flex-1 py-2.5 text-[13px] text-sand-300">
            Ask Argus
          </button>
        </nav>
      </header>
      {snapshot?.note && (
        <div className="border-b border-ink-800 bg-ink-900">
          <p className="mx-auto max-w-[1280px] px-4 md:px-8 py-2 text-[12px] text-sand-500">{snapshot.note}</p>
        </div>
      )}
      <main className="flex-1 mx-auto w-full max-w-[1280px] px-4 md:px-8 py-8 md:py-10">{children}</main>
      <PositionDrawer />
      <AskPanel />
    </div>
  );
}
