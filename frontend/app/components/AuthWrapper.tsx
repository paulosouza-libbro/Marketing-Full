"use client";

import { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";

export default function AuthWrapper({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [autenticado, setAutenticado] = useState<boolean | null>(null);
  const [usuario, setUsuario] = useState("");

  const isLoginPage = pathname === "/login";

  useEffect(() => {
    const token = localStorage.getItem("libbro_token");
    const user = localStorage.getItem("libbro_usuario") || "";
    if (!token && !isLoginPage) {
      router.replace("/login");
    } else {
      setAutenticado(!!token || isLoginPage);
      setUsuario(user);
    }
  }, [pathname]);

  const handleLogout = () => {
    localStorage.removeItem("libbro_token");
    localStorage.removeItem("libbro_usuario");
    document.cookie = "libbro_token=; path=/; max-age=0";
    router.replace("/login");
  };

  // Página de login — sem nav
  if (isLoginPage) return <main className="min-h-screen">{children}</main>;

  // Aguardando verificação
  if (autenticado === null) return (
    <div className="min-h-screen bg-zinc-950 flex items-center justify-center">
      <div className="text-zinc-600 text-sm">Verificando acesso...</div>
    </div>
  );

  // Não autenticado — redireciona (não renderiza nada)
  if (!autenticado) return null;

  return (
    <>
      <nav className="border-b border-zinc-800 px-6 py-4 flex items-center justify-between bg-zinc-950 sticky top-0 z-40">
        <div className="flex items-center gap-3">
          <span className="text-2xl">📣</span>
          <span className="font-bold text-lg">Libbro Marketing</span>
        </div>
        <div className="flex items-center gap-6 text-sm text-zinc-500">
          <a href="/" className="hover:text-white transition-colors">Dashboard</a>
          <a href="/campanhas" className="hover:text-white transition-colors">Campanhas</a>
          <a href="/aprovacoes" className="hover:text-white transition-colors">Aprovações</a>
          <a href="/assets" className="hover:text-white transition-colors">Assets</a>
          <a href="/analytics" className="hover:text-white transition-colors">Analytics</a>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-xs text-zinc-500">{usuario}</span>
          <button
            onClick={handleLogout}
            className="text-xs text-zinc-600 hover:text-red-400 px-3 py-1.5 rounded-lg hover:bg-zinc-800 transition-colors"
          >
            Sair
          </button>
        </div>
      </nav>
      <main className="min-h-screen bg-zinc-950">{children}</main>
    </>
  );
}
