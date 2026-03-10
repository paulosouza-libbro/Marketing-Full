"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

const API = process.env.NEXT_PUBLIC_API_URL || "https://libbro-marketing-production.up.railway.app";

export default function Login() {
  const router = useRouter();
  const [usuario, setUsuario] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setErro("");
    try {
      const res = await fetch(`${API}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuario, senha }),
      });
      if (!res.ok) { setErro("Usuário ou senha incorretos"); setLoading(false); return; }
      const data = await res.json();
      // Salva token em cookie (30 dias) e localStorage
      document.cookie = `libbro_token=${data.token}; path=/; max-age=${60*60*24*30}; SameSite=Strict`;
      localStorage.setItem("libbro_token", data.token);
      localStorage.setItem("libbro_usuario", data.usuario);
      router.push("/");
    } catch {
      setErro("Erro ao conectar. Tente novamente.");
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-zinc-950 flex items-center justify-center p-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="text-4xl mb-3">📣</div>
          <h1 className="text-2xl font-bold text-white">Libbro Marketing</h1>
          <p className="text-zinc-500 text-sm mt-1">Agência autônoma de marketing</p>
        </div>
        <form onSubmit={handleLogin} className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-1.5">Usuário</label>
            <input type="text" value={usuario} onChange={e => setUsuario(e.target.value)}
              placeholder="seu usuário" autoFocus
              className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-3 text-white placeholder-zinc-500 text-sm focus:outline-none focus:border-purple-500 transition-colors" />
          </div>
          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-1.5">Senha</label>
            <input type="password" value={senha} onChange={e => setSenha(e.target.value)}
              placeholder="••••••••"
              className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-3 text-white placeholder-zinc-500 text-sm focus:outline-none focus:border-purple-500 transition-colors" />
          </div>
          {erro && <div className="bg-red-950/40 border border-red-800/40 rounded-xl px-4 py-3 text-sm text-red-400">{erro}</div>}
          <button type="submit" disabled={!usuario || !senha || loading}
            className="w-full bg-purple-600 hover:bg-purple-500 disabled:opacity-40 text-white py-3 rounded-xl font-semibold text-sm transition-colors">
            {loading ? "Entrando..." : "Entrar"}
          </button>
        </form>
      </div>
    </div>
  );
}
