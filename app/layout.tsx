import type { Metadata, Viewport } from "next";
import "@fontsource/michroma/400.css";
import "@fontsource/ibm-plex-mono/400.css";
import "@fontsource/ibm-plex-mono/500.css";
import "@solana/wallet-adapter-react-ui/styles.css";
import "./globals.css";

export const metadata: Metadata = {
  title: { default: "Argus · A hundred eyes on your collateral", template: "%s · Argus" },
  description:
    "Argus never sleeps. It watches every Solana lending position and tells you what to do before the liquidators do.",
};

export const viewport: Viewport = { themeColor: "#16110c" };

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className="h-full">
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
