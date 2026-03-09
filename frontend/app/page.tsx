"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

const API = process.env.NEXT_PUBLIC_API_URL || "https://libbro-marketing-production.up.railway.app";

const AGENTES = [
  { id: "diretor", name: "Diretor", icon: "🎯", desc: "Planeja tasks a partir do briefing" },
  { id: "pesquisador_conto", name: "Pesquisador do Conto", icon: "📖", desc: "Origens, versões e curiosidades" },
  { id: "pesquisador", name: "Pesquisador", icon: "🔍", desc: "Mercado, tendências e benchmarks" },
  { id: "estrategista", name: "Estrategista", icon: "🗺️", desc: "Posicionamento e calendário" },
  { id: "copywriter", name: "Copywriter", icon: "✍️", desc: "Títulos, descrições, roteiros e hooks" },
  { id: "designer", name: "Designer", icon: "🎨", desc: "Thumbnails e artes visuais" },
  { id: "produtor_video", name: "Produtor de Vídeo", icon: "🎬", desc: "Roteiro e produção de vídeo" },
  { id: "seo_youtube", name: "SEO / YouTube", icon: "📈", desc: "Tags, palavras-chave, horário ideal" },
  { id: "social_media", name: "Social Media", icon: "📱", desc: "Adaptação para cada rede social" },
  { id: "growth", name: "Growth", icon: "⚡", desc: "Alavancas de crescimento sustentável" },
  { id: "analista", name: "Analista", icon: "📊", desc: "Performance e diagnósticos" },
];

const STATUS_COLORS: Record<string, string> = {
  processando: "text-blue-400",
  aguardando_aprovacao: "text-amber-400",
  concluida: "text-emerald-400",
  erro: "text-red-400",
};

const STATUS_LABEL: Record<string, string> = {
  processando: "Processando",
  aguardando_aprovacao: "Aguarda aprovação",
  concluida: "Concluída",
  erro: "Erro",
};

export default function Home() {
  const [campanhas, setCampanhas] = useState<any[]>([]);
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = () => {
    Promise.all([
      fetch(`${API}/campanhas`).then(r => r.json()).catch(() => []),
      fetch(`${API}/campanhas`).then(r => r.json())
        .then(async (camps) => {
          if (!Array.isArray(camps) || camps.length === 0) return [];
          const allTasks = await Promise.all(
            camps.map(c => fetch(`${API}/campanhas/${c.id}/tasks`).then(r => r.json()).catch(() => []))
          );
          return allTasks.flat();
        }).catch(() => []),
    ]).then(([camps, allTasks]) => {
      setCampanhas(Array.isArray(camps) ? camps : []);
      setTasks(Array.isArray(allTasks) ? allTasks : []);
      setLoading(false);
    });
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  const ativas = campanhas.filter(c => c.status === "processando").length;
  const aguardando = campanhas.filter(c => c.status === "aguardando_aprovacao").length;
  const tasksPendentes = tasks.filter(t => t.status === "aguardando_aprovacao");
  const recentes = [...campanhas].sort((a, b) => b.criado_em?.localeCompare(a.criado_em)).slice(0, 3);

  return (
    <div className="p-8 max-w-7xl mx-auto">

      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-1">Dashboard</h1>
        <p className="text-zinc-500">Agência de marketing autônoma da Libbro</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {[
          { label: "Campanhas Ativas", value: loading ? "—" : ativas, icon: "🚀", color: "text-blue-400" },
          { label: "Aguardando Aprovação", value: loading ? "—" : aguardando, icon: "⏳", color: "text-amber-400" },
          { label: "Tasks Pendentes", value: loading ? "—" : tasksPendentes.length, icon: "📋", color: "text-purple-400" },
          { label: "Agentes Disponíveis", value: AGENTES.length, icon: "🤖", color: "text-emerald-400" },
        ].map((stat) => (
          <div key={stat.label} className="bg-zinc-900 border border-zinc-800 rounded-xl p-5">
            <div className="text-2xl mb-2">{stat.icon}</div>
            <div className={`text-3xl font-bold mb-1 ${stat.color}`}>{stat.value}</div>
            <div className="text-sm text-zinc-500">{stat.label}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">

        {/* Tasks aguardando aprovação */}
        <div className="lg:col-span-1">
          <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-5 h-full">
            <h2 className="font-semibold mb-4 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse inline-block" />
              Aguardando sua aprovação
            </h2>
            {loading ? (
              <p className="text-zinc-600 text-sm">Carregando...</p>
            ) : tasksPendentes.length === 0 ? (
              <p className="text-zinc-600 text-sm">Nenhuma task aguardando</p>
            ) : (
              <div className="space-y-3">
                {tasksPendentes.slice(0, 4).map(task => {
                  const subtask = task.subtasks?.find((s: any) => s.status === "aguardando_aprovacao");
                  return (
                    <Link
                      key={task.id}
                      href={`/campanhas/${task.campanha_id}`}
                      className="block bg-amber-950/20 border border-amber-800/30 rounded-xl p-3 hover:border-amber-600/50 transition-colors"
                    >
                      <p className="text-sm font-medium text-amber-200">{task.titulo}</p>
                      {subtask && <p className="text-xs text-zinc-500 mt-0.5">{subtask.titulo}</p>}
                    </Link>
                  );
                })}
                {tasksPendentes.length > 4 && (
                  <p className="text-xs text-zinc-600">+{tasksPendentes.length - 4} mais</p>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Campanhas recentes */}
        <div className="lg:col-span-2">
          <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-5 h-full">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold">Campanhas Recentes</h2>
              <Link href="/campanhas" className="text-xs text-purple-400 hover:text-purple-300">Ver todas →</Link>
            </div>
            {loading ? (
              <p className="text-zinc-600 text-sm">Carregando...</p>
            ) : recentes.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-zinc-600 text-sm mb-3">Nenhuma campanha ainda</p>
                <Link href="/campanhas/nova" className="text-purple-400 text-sm hover:text-purple-300">
                  Criar primeira campanha →
                </Link>
              </div>
            ) : (
              <div className="space-y-3">
                {recentes.map(c => (
                  <Link
                    key={c.id}
                    href={`/campanhas/${c.id}`}
                    className="flex items-center justify-between p-3 bg-zinc-800/50 hover:bg-zinc-800 rounded-xl transition-colors group"
                  >
                    <div>
                      <p className="text-sm font-medium capitalize group-hover:text-purple-300 transition-colors">{c.conto}</p>
                      <p className="text-xs text-zinc-500 line-clamp-1 mt-0.5">{c.briefing}</p>
                    </div>
                    <span className={`text-xs shrink-0 ml-3 ${STATUS_COLORS[c.status] || "text-zinc-500"}`}>
                      {STATUS_LABEL[c.status] || c.status}
                    </span>
                  </Link>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Quick action */}
      <div className="bg-gradient-to-r from-purple-900/30 to-zinc-900 border border-purple-700/30 rounded-2xl p-6 mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold mb-1">Nova Campanha</h2>
            <p className="text-zinc-500 text-sm">Dê o briefing — o Diretor planeja as tasks e os agentes executam</p>
          </div>
          <Link href="/campanhas/nova" className="bg-purple-600 hover:bg-purple-500 text-white px-6 py-3 rounded-xl font-medium transition-colors shrink-0">
            Começar →
          </Link>
        </div>
      </div>

      {/* Agentes */}
      <div>
        <h2 className="text-lg font-semibold mb-4">
          Equipe de Agentes
          <span className="text-zinc-600 font-normal text-sm ml-2">({AGENTES.length} disponíveis)</span>
        </h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
          {AGENTES.map((agent) => (
            <div
              key={agent.id}
              className="bg-zinc-900 border border-zinc-800 hover:border-zinc-600 rounded-xl p-4 transition-colors"
            >
              <div className="text-2xl mb-2">{agent.icon}</div>
              <div className="font-medium text-xs mb-1 leading-tight">{agent.name}</div>
              <div className="text-xs text-zinc-600 leading-tight">{agent.desc}</div>
              <div className="mt-2 flex items-center gap-1">
                <div className="w-1.5 h-1.5 rounded-full bg-emerald-500"></div>
                <span className="text-xs text-zinc-600">Pronto</span>
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
