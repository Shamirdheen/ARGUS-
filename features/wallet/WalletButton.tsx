"use client";

import { useWallet } from "@solana/wallet-adapter-react";
import { useWalletModal } from "@solana/wallet-adapter-react-ui";
import { Wallet } from "@phosphor-icons/react";
import { Button } from "@/components/ui";

export function WalletButton({ small = true, label = "Connect wallet" }: { small?: boolean; label?: string }) {
  const { publicKey, disconnect, connecting } = useWallet();
  const { setVisible } = useWalletModal();

  if (publicKey) {
    const k = publicKey.toBase58();
    return (
      <Button kind="secondary" small={small} onClick={() => disconnect()} title="Disconnect">
        <Wallet size={16} weight="light" aria-hidden />
        {k.slice(0, 4)}…{k.slice(-4)}
      </Button>
    );
  }
  return (
    <Button kind="primary" small={small} onClick={() => setVisible(true)} disabled={connecting}>
      <Wallet size={16} weight="light" aria-hidden />
      {connecting ? "Connecting…" : label}
    </Button>
  );
}
