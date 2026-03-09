"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

const API = process.env.NEXT_PUBLIC_API_URL || "https://libbro-marketing-production.up.railway.app";

export default function NovaCampanha() {
  const router = useRouter();
  const [briefing, setBriefing] = useState("");
  const [conto, setConto] = useState("");
  const [canais, setCanais] = useState<string[]>(["youtube"]);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");
  const [contos, setContos] = useState<{slug: string, nome: string}[]>([]);

  const CONTOS_PADRAO = [
    { slug: "cinderela", nome: "Cinderela" },
    { slug: "joao-e-maria", nome: "João e Maria" },
    { slug: "o-camponesinho-no-ceu", nome: "O Camponesinho no Céu" },
    { slug: "chapeuzinho-vermelho", nome: "Chapeuzinho Vermelho" },
    { slug: "o-pequeno-polegar", nome: "O Pequeno Polegar" },
  ];

  useEffect(() => {
    fetch(`${API}/contos`)
      .then(r => r.json())
      .then(data => setContos(Array.isArray(data) && data.length > 0 ? data : CONTOS_PADRAO))
      .catch(() => setContos(CONTOS_PADRAO));
  }, []);

  const toggleCanal = (canal: string) => {
    setCanais(prev =>
      prev.includes(canal) ? prev.filter(c => c !== canal) : [...prev, canal]
    );
  };

  const handleSubmit = async () => {
    if (!briefing || !conto) return;
    setLoading(true);
    setErro("");

    try {
      const res = await fetch(`${API}/campanhas`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ briefing, conto, canais }),
      });

      if (!res.ok) throw new Error(`Erro ${res.status}`);

      const data = await res.json();
      router.push(`/campanhas/${data.id}`);
    } catch (e: any) {
      setErro("Erro ao criar campanha. Tente novamente.");
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <div className="mb-8">
        <a href="/campanhas" className="text-zinc-500 hover:text-white text-sm">← Campanhas</a>
        <h1 className="text-3xl font-bold mt-2 mb-1">Nova Campanha</h1>
        <p className="text-zinc-500">Dê o briefing inicial — os agentes cuidam do resto</p>
      </div>

      <div className="space-y-6">

        {/* Briefing */}
        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
          <label className="block font-medium mb-3">
            🎯 Briefing da Campanha
            <span className="text-red-500 ml-1">*</span>
          </label>
          <textarea
            value={briefing}
            onChange={e => setBriefing(e.target.value)}
            placeholder="Ex: Quero lançar a Cinderela no YouTube com foco em pais de crianças de 3 a 8 anos. Preciso de thumbnail, copy do vídeo e post no Instagram..."
            className="w-full bg-zinc-950 border border-zinc-700 rounded-lg p-4 text-sm resize-none h-36 focus:outline-none focus:border-purple-600 text-white placeholder-zinc-600"
          />
          <p className="text-xs text-zinc-600 mt-2">{briefing.length} caracteres — quanto mais detalhe, melhores as tasks geradas pelo Diretor</p>
        </div>

        {/* Conto */}
        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
          <label className="block font-medium mb-3">
            📖 Conto
            <span className="text-red-500 ml-1">*</span>
          </label>
          <select
            value={conto}
            onChange={e => setConto(e.target.value)}
            className="w-full bg-zinc-950 border border-zinc-700 rounded-lg p-3 text-sm focus:outline-none focus:border-purple-600 text-white"
          >
            <option value="">Selecione um conto</option>
            {contos.map(c => (
              <option key={c.slug} value={c.slug}>{c.nome}</option>
            ))}
          </select>
          <p className="text-xs text-zinc-600 mt-2">
            O Designer usará as referências visuais deste conto automaticamente.
          </p>
        </div>

        {/* Canais */}
        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
          <label className="block font-medium mb-3">📡 Canais</label>
          <div className="flex flex-wrap gap-3">
            {[
              { id: "youtube", label: "YouTube", icon: "▶️" },
              { id: "instagram", label: "Instagram", icon: "📸" },
              { id: "tiktok", label: "TikTok", icon: "🎵" },
              { id: "twitter", label: "Twitter/X", icon: "🐦" },
              { id: "facebook", label: "Facebook", icon: "👥" },
              { id: "email", label: "E-mail", icon: "📧" },
            ].map(canal => (
              <button
                key={canal.id}
                onClick={() => toggleCanal(canal.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm border transition-colors ${
                  canais.includes(canal.id)
                    ? "bg-purple-900/30 border-purple-600 text-white"
                    : "bg-zinc-950 border-zinc-700 text-zinc-500 hover:border-zinc-500"
                }`}
              >
                <span>{canal.icon}</span>
                {canal.label}
              </button>
            ))}
          </div>
        </div>

        {/* Erro */}
        {erro && (
          <div className="bg-red-950/30 border border-red-800 rounded-xl px-4 py-3 text-sm text-red-400">
            {erro}
          </div>
        )}

        {/* Submit */}
        <button
          onClick={handleSubmit}
          disabled={!briefing || !conto || loading}
          className="w-full bg-purple-600 hover:bg-purple-500 disabled:bg-zinc-800 disabled:text-zinc-600 text-white py-4 rounded-xl font-medium transition-colors text-lg"
        >
          {loading ? "🤖 Criando campanha..." : "🚀 Iniciar Campanha"}
        </button>

        <p className="text-center text-xs text-zinc-600">
          ⚠️ Todo conteúdo gerado passará pela sua aprovação antes de publicar
        </p>
      </div>
    </div>
  );
}
