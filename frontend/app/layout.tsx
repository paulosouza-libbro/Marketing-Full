import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "./globals.css";
import AuthWrapper from "./components/AuthWrapper";

const geist = Geist({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Libbro Marketing",
  description: "Agência de Marketing Autônoma da Libbro",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body className={geist.className}>
        <AuthWrapper>{children}</AuthWrapper>
      </body>
    </html>
  );
}
