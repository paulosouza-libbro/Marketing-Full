"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

const contos = [
  { slug: "exemplo-conto", nome: "Exemplo Conto" },
];

export default function NovaCampanha() {
  const router = useRouter();
  const [briefing, setBriefing] = useState("");
  const [conto, setConto] = useState("");
  const [canais, setCanais] = useState<string[]>(["youtube"]);
  const [loading, setLoading] = useState(false);

  const toggleCanal = (canal: string) => {
    setCanais(prev =>
      prev.includes(canal) ? prev.filter(c => c !== canal) : [...prev, canal]
    );
  };

  const handleSubmit = async () => {
    if (!briefing || !conto) return;
    setLoading(true);
    // TODO: Chamar API do backend
    setTimeout(() => {
      setLoading(false);
      router.push("/campanhas");
    }, 2000);
  };

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <div className="mb-8">
        <a href="/campanhas" className="text-[#6b7280] hover:text-white text-sm">← Campanhas</a>
        <h1 className="text-3xl font-bold mt-2 mb-1">Nova Campanha</h1>
        <p className="text-[#6b7280]">Dê o briefing inicial — os agentes cuidam do resto</p>
      </div>

      <div className="space-y-6">

        {/* Briefing */}
        <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl p-6">
          <label className="block font-medium mb-3">
            🎯 Briefing da Campanha
            <span className="text-[#ef4444] ml-1">*</span>
          </label>
          <textarea
            value={briefing}
            onChange={e => setBriefing(e.target.value)}
            placeholder="Ex: Quero divulgar o conto X para um público jovem adulto no YouTube, com foco em gerar inscritos e visualizações orgânicas..."
            className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg p-4 text-sm resize-none h-32 focus:outline-none focus:border-[#7c3aed] text-white placeholder-[#4b5563]"
          />
        </div>

        {/* Conto */}
        <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl p-6">
          <label className="block font-medium mb-3">
            📖 Conto
            <span className="text-[#ef4444] ml-1">*</span>
          </label>
          <select
            value={conto}
            onChange={e => setConto(e.target.value)}
            className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg p-3 text-sm focus:outline-none focus:border-[#7c3aed] text-white"
          >
            <option value="">Selecione um conto</option>
            {contos.map(c => (
              <option key={c.slug} value={c.slug}>{c.nome}</option>
            ))}
          </select>
          <p className="text-xs text-[#6b7280] mt-2">
            O Designer usará as referências visuais deste conto automaticamente.
          </p>
        </div>

        {/* Canais */}
        <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl p-6">
          <label className="block font-medium mb-3">📡 Canais</label>
          <div className="flex flex-wrap gap-3">
            {[
              { id: "youtube", label: "YouTube", icon: "▶️" },
              { id: "instagram", label: "Instagram", icon: "📸" },
              { id: "tiktok", label: "TikTok", icon: "🎵" },
              { id: "twitter", label: "Twitter/X", icon: "🐦" },
              { id: "facebook", label: "Facebook", icon: "👥" },
            ].map(canal => (
              <button
                key={canal.id}
                onClick={() => toggleCanal(canal.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm border transition-colors ${
                  canais.includes(canal.id)
                    ? "bg-[#7c3aed]/20 border-[#7c3aed] text-white"
                    : "bg-[#0f0f0f] border-[#2a2a2a] text-[#6b7280] hover:border-[#4b5563]"
                }`}
              >
                <span>{canal.icon}</span>
                {canal.label}
              </button>
            ))}
          </div>
        </div>

        {/* Submit */}
        <button
          onClick={handleSubmit}
          disabled={!briefing || !conto || loading}
          className="w-full bg-[#7c3aed] hover:bg-[#6d28d9] disabled:bg-[#2a2a2a] disabled:text-[#6b7280] text-white py-4 rounded-xl font-medium transition-colors text-lg"
        >
          {loading ? "🤖 Agentes trabalhando..." : "🚀 Iniciar Campanha"}
        </button>

        <p className="text-center text-xs text-[#6b7280]">
          ⚠️ Todo conteúdo gerado passará pela sua aprovação antes de publicar
        </p>
      </div>
    </div>
  );
}
