"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

const API = process.env.NEXT_PUBLIC_API_URL || "https://libbro-marketing-production.up.railway.app";

const STATUS_COLORS: Record<string, string> = {
  processando: "bg-blue-900/40 text-blue-300",
  aguardando_aprovacao: "bg-amber-900/40 text-amber-300",
  concluida: "bg-emerald-900/40 text-emerald-300",
  erro: "bg-red-900/40 text-red-300",
};

const STATUS_LABEL: Record<string, string> = {
  processando: "Processando",
  aguardando_aprovacao: "Aguarda aprovação",
  concluida: "Concluída",
  erro: "Erro",
};

export default function Campanhas() {
  const [campanhas, setCampanhas] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/campanhas`)
      .then((r) => r.json())
      .then((data) => { setCampanhas(Array.isArray(data) ? data : []); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div className="p-8 max-w-7xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold mb-1">Campanhas</h1>
          <p className="text-zinc-500">Histórico e status de todas as campanhas</p>
        </div>
        <Link href="/campanhas/nova" className="bg-purple-600 hover:bg-purple-500 text-white px-5 py-2.5 rounded-lg font-medium transition-colors">
          + Nova Campanha
        </Link>
      </div>

      {loading ? (
        <div className="text-zinc-500 text-center py-16">Carregando...</div>
      ) : campanhas.length === 0 ? (
        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-16 text-center">
          <div className="text-5xl mb-4">🚀</div>
          <h2 className="text-xl font-bold mb-2">Nenhuma campanha ainda</h2>
          <p className="text-zinc-500 mb-6">Crie sua primeira campanha e deixe os agentes trabalharem</p>
          <Link href="/campanhas/nova" className="bg-purple-600 hover:bg-purple-500 text-white px-6 py-3 rounded-lg font-medium transition-colors inline-block">
            Criar Primeira Campanha
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {campanhas.map((c) => (
            <Link
              key={c.id}
              href={`/campanhas/${c.id}`}
              className="bg-zinc-900 border border-zinc-800 hover:border-zinc-600 rounded-2xl p-5 transition-all group"
            >
              <div className="flex items-start justify-between mb-3">
                <h3 className="font-semibold capitalize group-hover:text-purple-300 transition-colors">{c.conto}</h3>
                <span className={`text-xs px-2 py-0.5 rounded-full ${STATUS_COLORS[c.status] || "bg-zinc-800 text-zinc-400"}`}>
                  {STATUS_LABEL[c.status] || c.status}
                </span>
              </div>
              <p className="text-zinc-500 text-xs line-clamp-2 mb-4">{c.briefing}</p>
              <div className="flex items-center justify-between">
                <div className="flex gap-1">
                  {c.canais?.map((canal: string) => (
                    <span key={canal} className="text-xs bg-zinc-800 text-zinc-400 px-2 py-0.5 rounded-full">{canal}</span>
                  ))}
                </div>
                <span className="text-zinc-600 text-xs">{new Date(c.criado_em).toLocaleDateString("pt-BR")}</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
