import { WalletProviders } from "@/features/wallet/WalletProviders";
import "@/features/wallet/wallet-adapter.css";
import { PortfolioProvider } from "@/features/portfolio/PortfolioProvider";
import { AppShell } from "@/features/shell/AppShell";

export default function AppLayout({ children }: LayoutProps<"/app">) {
  return (
    <WalletProviders>
      <PortfolioProvider>
        <AppShell>{children}</AppShell>
      </PortfolioProvider>
    </WalletProviders>
  );
}
