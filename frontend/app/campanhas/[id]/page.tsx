"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";

const API = process.env.NEXT_PUBLIC_API_URL || "https://libbro-marketing-production.up.railway.app";

const AGENTE_ICONS: Record<string, string> = {
  pesquisador_conto: "🔍",
  copywriter: "✍️",
  designer: "🎨",
  seo_youtube: "📈",
  social_media: "📱",
  produtor_video: "🎬",
  analista: "📊",
  diretor: "🎯",
  estrategista: "🗺️",
  growth: "⚡",
};

const STATUS_COLORS: Record<string, string> = {
  pendente: "bg-zinc-800 text-zinc-400",
  executando: "bg-blue-900/50 text-blue-300 animate-pulse",
  aguardando_aprovacao: "bg-amber-900/50 text-amber-300",
  aprovada: "bg-emerald-900/50 text-emerald-300",
  concluida: "bg-emerald-900/50 text-emerald-300",
  rejeitada: "bg-red-900/50 text-red-300",
  erro: "bg-red-900/50 text-red-300",
};

const STATUS_LABEL: Record<string, string> = {
  pendente: "Pendente",
  executando: "Executando...",
  aguardando_aprovacao: "Aguarda aprovação",
  aprovada: "Aprovada",
  concluida: "Concluída",
  rejeitada: "Rejeitada",
  erro: "Erro",
};

export default function CampanhaDetalhe() {
  const params = useParams();
  const router = useRouter();
  const campanhaId = params.id as string;

  const [campanha, setCampanha] = useState<any>(null);
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [gerandoTasks, setGerandoTasks] = useState(false);
  const [feedbackMap, setFeedbackMap] = useState<Record<string, string>>({});

  // Modal de nova task manual
  const [showModal, setShowModal] = useState(false);
  const [novaTask, setNovaTask] = useState({ titulo: "", descricao: "" });
  const [novasSubtasks, setNovasSubtasks] = useState([
    { titulo: "", descricao: "", agente: "copywriter", requer_aprovacao: true },
  ]);

  const fetchData = async () => {
    const [c, t] = await Promise.all([
      fetch(`${API}/campanhas/${campanhaId}`).then((r) => r.json()),
      fetch(`${API}/campanhas/${campanhaId}/tasks`).then((r) => r.json()),
    ]);
    setCampanha(c);
    setTasks(Array.isArray(t) ? t : []);
    setLoading(false);
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000); // polling a cada 5s
    return () => clearInterval(interval);
  }, [campanhaId]);

  const gerarTasks = async () => {
    setGerandoTasks(true);
    await fetch(`${API}/campanhas/${campanhaId}/tasks/gerar`, { method: "POST" });
    await fetchData();
    setGerandoTasks(false);
  };

  const aprovarSubtask = async (taskId: string, subtaskId: string, action: "approve" | "reject") => {
    const feedback = feedbackMap[subtaskId] || "";
    await fetch(`${API}/campanhas/${campanhaId}/tasks/${taskId}/subtasks/${subtaskId}/aprovar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action, feedback }),
    });
    await fetchData();
  };

  const removerTask = async (taskId: string) => {
    if (!confirm("Remover esta task?")) return;
    await fetch(`${API}/campanhas/${campanhaId}/tasks/${taskId}`, { method: "DELETE" });
    await fetchData();
  };

  const adicionarTask = async () => {
    await fetch(`${API}/campanhas/${campanhaId}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...novaTask, subtasks: novasSubtasks }),
    });
    setShowModal(false);
    setNovaTask({ titulo: "", descricao: "" });
    setNovasSubtasks([{ titulo: "", descricao: "", agente: "copywriter", requer_aprovacao: true }]);
    await fetchData();
  };

  if (loading) return <div className="min-h-screen bg-zinc-950 flex items-center justify-center text-zinc-400">Carregando...</div>;
  if (!campanha) return <div className="min-h-screen bg-zinc-950 flex items-center justify-center text-red-400">Campanha não encontrada</div>;

  const hasTasks = tasks.length > 0;

  return (
    <div className="min-h-screen bg-zinc-950 text-white">
      {/* Header */}
      <div className="border-b border-zinc-800 px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link href="/campanhas" className="text-zinc-500 hover:text-white text-sm">← Campanhas</Link>
            <span className="text-zinc-700">/</span>
            <span className="text-sm text-zinc-300">{campanha.conto}</span>
          </div>
          <button
            onClick={() => setShowModal(true)}
            className="bg-zinc-800 hover:bg-zinc-700 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            + Adicionar task
          </button>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-8">
        {/* Briefing */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold mb-1 capitalize">{campanha.conto}</h1>
          <p className="text-zinc-400 text-sm mb-3">Campanha · {campanha.canais?.join(", ")}</p>
          <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4 text-sm text-zinc-300 leading-relaxed">
            {campanha.briefing}
          </div>
        </div>

        {/* Tasks */}
        {!hasTasks ? (
          <div className="text-center py-16 border border-dashed border-zinc-800 rounded-2xl">
            <p className="text-zinc-500 mb-2 text-lg">Nenhuma task ainda</p>
            <p className="text-zinc-600 text-sm mb-6">O Diretor pode gerar as tasks automaticamente a partir do briefing.</p>
            <button
              onClick={gerarTasks}
              disabled={gerandoTasks}
              className="bg-purple-600 hover:bg-purple-500 disabled:opacity-50 px-6 py-3 rounded-xl font-semibold transition-colors"
            >
              {gerandoTasks ? "🎯 Diretor planejando..." : "🎯 Gerar tasks com o Diretor"}
            </button>
          </div>
        ) : (
          <>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">Tasks <span className="text-zinc-500 font-normal text-sm">({tasks.length})</span></h2>
              <button
                onClick={gerarTasks}
                disabled={gerandoTasks}
                className="text-xs text-zinc-500 hover:text-zinc-300 transition-colors"
              >
                {gerandoTasks ? "planejando..." : "↻ Regerar tasks"}
              </button>
            </div>

            {/* Grid de tasks (paralelas) */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {tasks.map((task) => {
                const concluidas = task.subtasks?.filter((s: any) => ["concluida", "aprovada"].includes(s.status)).length || 0;
                const total = task.subtasks?.length || 0;
                const pct = total ? Math.round(concluidas / total * 100) : 0;

                return (
                  <div key={task.id} className="bg-zinc-900 border border-zinc-800 rounded-2xl overflow-hidden">
                    {/* Task header */}
                    <div className="p-4 border-b border-zinc-800 flex items-start justify-between gap-2">
                      <div>
                        <h3 className="font-semibold text-sm">{task.titulo}</h3>
                        <p className="text-zinc-500 text-xs mt-0.5">{task.descricao}</p>
                      </div>
                      <div className="flex items-center gap-2 shrink-0">
                        <span className={`text-xs px-2 py-0.5 rounded-full ${STATUS_COLORS[task.status] || "bg-zinc-800 text-zinc-400"}`}>
                          {STATUS_LABEL[task.status] || task.status}
                        </span>
                        <button
                          onClick={() => removerTask(task.id)}
                          className="text-zinc-700 hover:text-red-400 text-xs transition-colors"
                          title="Remover task"
                        >✕</button>
                      </div>
                    </div>

                    {/* Progress bar */}
                    {total > 0 && (
                      <div className="px-4 pt-3">
                        <div className="flex justify-between text-xs text-zinc-500 mb-1">
                          <span>{concluidas}/{total} subtasks</span>
                          <span>{pct}%</span>
                        </div>
                        <div className="h-1 bg-zinc-800 rounded-full">
                          <div className="h-1 bg-purple-500 rounded-full transition-all" style={{ width: `${pct}%` }} />
                        </div>
                      </div>
                    )}

                    {/* Subtasks */}
                    <div className="p-4 space-y-3">
                      {task.subtasks?.map((sub: any, idx: number) => (
                        <div
                          key={sub.id}
                          className={`rounded-xl border p-3 transition-all ${
                            sub.status === "aguardando_aprovacao"
                              ? "border-amber-700/50 bg-amber-950/20"
                              : sub.status === "executando"
                              ? "border-blue-700/50 bg-blue-950/20"
                              : sub.status === "aprovada" || sub.status === "concluida"
                              ? "border-emerald-800/30 bg-emerald-950/10"
                              : sub.status === "rejeitada"
                              ? "border-red-800/30 bg-red-950/10"
                              : "border-zinc-800 bg-zinc-900/50"
                          }`}
                        >
                          <div className="flex items-start gap-2">
                            <span className="text-base mt-0.5">{AGENTE_ICONS[sub.agente] || "🤖"}</span>
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2 flex-wrap">
                                <span className="text-xs font-medium">{sub.titulo}</span>
                                <span className={`text-xs px-1.5 py-0.5 rounded-full ${STATUS_COLORS[sub.status] || "bg-zinc-800 text-zinc-400"}`}>
                                  {STATUS_LABEL[sub.status] || sub.status}
                                </span>
                              </div>
                              <p className="text-zinc-500 text-xs mt-0.5 truncate">{sub.agente}</p>

                              {/* Output da subtask */}
                              {sub.output && (
                                <p className="text-zinc-400 text-xs mt-2 leading-relaxed border-l-2 border-zinc-700 pl-2">
                                  {sub.output}
                                </p>
                              )}

                              {/* Botões de aprovação */}
                              {sub.status === "aguardando_aprovacao" && (
                                <div className="mt-3 space-y-2">
                                  <textarea
                                    placeholder="Feedback (opcional para aprovação, obrigatório para rejeição)"
                                    className="w-full bg-zinc-800 border border-zinc-700 rounded-lg px-3 py-2 text-xs text-white placeholder-zinc-500 resize-none"
                                    rows={2}
                                    value={feedbackMap[sub.id] || ""}
                                    onChange={(e) => setFeedbackMap({ ...feedbackMap, [sub.id]: e.target.value })}
                                  />
                                  <div className="flex gap-2">
                                    <button
                                      onClick={() => aprovarSubtask(task.id, sub.id, "approve")}
                                      className="flex-1 bg-emerald-700 hover:bg-emerald-600 text-white text-xs py-1.5 rounded-lg font-medium transition-colors"
                                    >
                                      ✓ Aprovar
                                    </button>
                                    <button
                                      onClick={() => aprovarSubtask(task.id, sub.id, "reject")}
                                      className="flex-1 bg-red-900 hover:bg-red-800 text-white text-xs py-1.5 rounded-lg font-medium transition-colors"
                                    >
                                      ✕ Rejeitar
                                    </button>
                                  </div>
                                </div>
                              )}

                              {/* Feedback de rejeição */}
                              {sub.status === "rejeitada" && sub.feedback_rejeicao && (
                                <p className="text-red-400 text-xs mt-2 italic">"{sub.feedback_rejeicao}"</p>
                              )}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          </>
        )}
      </div>

      {/* Modal: nova task manual */}
      {showModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-zinc-900 border border-zinc-700 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <h2 className="text-lg font-bold mb-4">Nova task</h2>

              <div className="space-y-4">
                <input
                  placeholder="Título da task (ex: Post Instagram)"
                  className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-3 text-sm text-white placeholder-zinc-500"
                  value={novaTask.titulo}
                  onChange={(e) => setNovaTask({ ...novaTask, titulo: e.target.value })}
                />
                <textarea
                  placeholder="Descrição geral da task"
                  className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-3 text-sm text-white placeholder-zinc-500 resize-none"
                  rows={2}
                  value={novaTask.descricao}
                  onChange={(e) => setNovaTask({ ...novaTask, descricao: e.target.value })}
                />

                <div>
                  <p className="text-xs text-zinc-400 mb-2 font-medium">Subtasks (sequenciais)</p>
                  {novasSubtasks.map((sub, idx) => (
                    <div key={idx} className="border border-zinc-700 rounded-xl p-3 mb-2 space-y-2">
                      <div className="flex gap-2 items-center">
                        <span className="text-zinc-500 text-xs w-4">{idx + 1}.</span>
                        <input
                          placeholder="Título da subtask"
                          className="flex-1 bg-zinc-800 border border-zinc-700 rounded-lg px-3 py-2 text-xs text-white placeholder-zinc-500"
                          value={sub.titulo}
                          onChange={(e) => {
                            const updated = [...novasSubtasks];
                            updated[idx].titulo = e.target.value;
                            setNovasSubtasks(updated);
                          }}
                        />
                        {novasSubtasks.length > 1 && (
                          <button
                            onClick={() => setNovasSubtasks(novasSubtasks.filter((_, i) => i !== idx))}
                            className="text-zinc-600 hover:text-red-400 text-xs"
                          >✕</button>
                        )}
                      </div>
                      <textarea
                        placeholder="Instrução para o agente"
                        className="w-full bg-zinc-800 border border-zinc-700 rounded-lg px-3 py-2 text-xs text-white placeholder-zinc-500 resize-none"
                        rows={2}
                        value={sub.descricao}
                        onChange={(e) => {
                          const updated = [...novasSubtasks];
                          updated[idx].descricao = e.target.value;
                          setNovasSubtasks(updated);
                        }}
                      />
                      <div className="flex gap-3 items-center">
                        <select
                          className="bg-zinc-800 border border-zinc-700 rounded-lg px-2 py-1.5 text-xs text-white"
                          value={sub.agente}
                          onChange={(e) => {
                            const updated = [...novasSubtasks];
                            updated[idx].agente = e.target.value;
                            setNovasSubtasks(updated);
                          }}
                        >
                          {Object.entries(AGENTE_ICONS).map(([id, icon]) => (
                            <option key={id} value={id}>{icon} {id}</option>
                          ))}
                        </select>
                        <label className="flex items-center gap-1.5 text-xs text-zinc-400 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={sub.requer_aprovacao}
                            onChange={(e) => {
                              const updated = [...novasSubtasks];
                              updated[idx].requer_aprovacao = e.target.checked;
                              setNovasSubtasks(updated);
                            }}
                            className="accent-purple-500"
                          />
                          Requer aprovação
                        </label>
                      </div>
                    </div>
                  ))}
                  <button
                    onClick={() => setNovasSubtasks([...novasSubtasks, { titulo: "", descricao: "", agente: "copywriter", requer_aprovacao: true }])}
                    className="text-xs text-purple-400 hover:text-purple-300 mt-1"
                  >
                    + Adicionar subtask
                  </button>
                </div>
              </div>

              <div className="flex gap-3 mt-6">
                <button
                  onClick={() => setShowModal(false)}
                  className="flex-1 bg-zinc-800 hover:bg-zinc-700 py-3 rounded-xl text-sm font-medium transition-colors"
                >
                  Cancelar
                </button>
                <button
                  onClick={adicionarTask}
                  disabled={!novaTask.titulo}
                  className="flex-1 bg-purple-600 hover:bg-purple-500 disabled:opacity-40 py-3 rounded-xl text-sm font-semibold transition-colors"
                >
                  Criar task
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
