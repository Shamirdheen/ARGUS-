"use client";

import { ConnectionProvider, WalletProvider } from "@solana/wallet-adapter-react";
import { WalletModalProvider } from "@solana/wallet-adapter-react-ui";
import type { ReactNode } from "react";

const RPC = process.env.NEXT_PUBLIC_SOLANA_RPC_URL ?? "https://api.mainnet-beta.solana.com";

/**
 * Phantom, Solflare, Backpack etc. register themselves through the Wallet Standard,
 * so no per-wallet adapters are bundled. Argus only ever asks for the public key.
 */
export function WalletProviders({ children }: { children: ReactNode }) {
  return (
    <ConnectionProvider endpoint={RPC}>
      <WalletProvider wallets={[]} autoConnect>
        <WalletModalProvider>{children}</WalletModalProvider>
      </WalletProvider>
    </ConnectionProvider>
  );
}
