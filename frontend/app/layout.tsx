import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "./globals.css";

const geist = Geist({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Libbro Marketing",
  description: "Agência de Marketing Autônoma da Libbro",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body className={geist.className}>
        <nav className="border-b border-[#2a2a2a] px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl">📣</span>
            <span className="font-bold text-lg">Libbro Marketing</span>
          </div>
          <div className="flex items-center gap-6 text-sm text-[#6b7280]">
            <a href="/" className="hover:text-white transition-colors">Dashboard</a>
            <a href="/campanhas" className="hover:text-white transition-colors">Campanhas</a>
            <a href="/aprovacoes" className="hover:text-white transition-colors">Aprovações</a>
            <a href="/assets" className="hover:text-white transition-colors">Assets</a>
            <a href="/analytics" className="hover:text-white transition-colors">Analytics</a>
          </div>
        </nav>
        <main className="min-h-screen">
          {children}
        </main>
      </body>
    </html>
  );
}
