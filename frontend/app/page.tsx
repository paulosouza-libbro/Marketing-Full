import Link from "next/link";

const stats = [
  { label: "Campanhas Ativas", value: "0", icon: "🚀" },
  { label: "Aguardando Aprovação", value: "0", icon: "⏳" },
  { label: "Publicados Este Mês", value: "0", icon: "✅" },
  { label: "Agentes Online", value: "10", icon: "🤖" },
];

const agents = [
  { name: "Diretor", icon: "🎯", status: "idle", desc: "Coordenação e estratégia" },
  { name: "Pesquisador", icon: "🔍", status: "idle", desc: "Mercado e tendências" },
  { name: "Estrategista", icon: "🗺️", status: "idle", desc: "Posicionamento e funil" },
  { name: "Copywriter", icon: "✍️", status: "idle", desc: "Textos e roteiros" },
  { name: "Designer", icon: "🎨", status: "idle", desc: "Imagens e thumbnails" },
  { name: "Produtor de Vídeo", icon: "🎬", status: "idle", desc: "Vídeos para YouTube" },
  { name: "SEO/YouTube", icon: "📈", status: "idle", desc: "Otimização e ranqueamento" },
  { name: "Social Media", icon: "📱", status: "idle", desc: "Redes sociais" },
  { name: "Growth", icon: "⚡", status: "idle", desc: "Experimentos e crescimento" },
  { name: "Analista", icon: "📊", status: "idle", desc: "Performance e relatórios" },
];

export default function Home() {
  return (
    <div className="p-8 max-w-7xl mx-auto">

      {/* Header */}
      <div className="mb-10">
        <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
        <p className="text-[#6b7280]">Visão geral da sua agência de marketing autônoma</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
        {stats.map((stat) => (
          <div key={stat.label} className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl p-5">
            <div className="text-2xl mb-2">{stat.icon}</div>
            <div className="text-3xl font-bold mb-1">{stat.value}</div>
            <div className="text-sm text-[#6b7280]">{stat.label}</div>
          </div>
        ))}
      </div>

      {/* Quick Action */}
      <div className="bg-gradient-to-r from-[#7c3aed]/20 to-[#1a1a1a] border border-[#7c3aed]/30 rounded-xl p-6 mb-10">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold mb-1">Nova Campanha</h2>
            <p className="text-[#6b7280] text-sm">Dê o briefing e os agentes cuidam do resto</p>
          </div>
          <Link
            href="/campanhas/nova"
            className="bg-[#7c3aed] hover:bg-[#6d28d9] text-white px-6 py-3 rounded-lg font-medium transition-colors"
          >
            Começar →
          </Link>
        </div>
      </div>

      {/* Agents Grid */}
      <div>
        <h2 className="text-xl font-bold mb-4">Equipe de Agentes</h2>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
          {agents.map((agent) => (
            <div key={agent.name} className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl p-4 hover:border-[#7c3aed]/50 transition-colors">
              <div className="text-2xl mb-2">{agent.icon}</div>
              <div className="font-medium text-sm mb-1">{agent.name}</div>
              <div className="text-xs text-[#6b7280]">{agent.desc}</div>
              <div className="mt-2 flex items-center gap-1">
                <div className="w-2 h-2 rounded-full bg-[#10b981]"></div>
                <span className="text-xs text-[#6b7280]">Pronto</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
