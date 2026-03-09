export default function Analytics() {
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-1">Analytics</h1>
        <p className="text-[#6b7280]">Desempenho das campanhas e insights do Analista</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {[
          { label: "Views Totais", value: "—", icon: "👁️" },
          { label: "Watch Time", value: "—", icon: "⏱️" },
          { label: "CTR Médio", value: "—", icon: "🖱️" },
          { label: "Novos Inscritos", value: "—", icon: "📧" },
        ].map(metric => (
          <div key={metric.label} className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl p-5">
            <div className="text-2xl mb-2">{metric.icon}</div>
            <div className="text-2xl font-bold mb-1">{metric.value}</div>
            <div className="text-sm text-[#6b7280]">{metric.label}</div>
          </div>
        ))}
      </div>

      <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl p-16 text-center">
        <div className="text-5xl mb-4">📊</div>
        <h2 className="text-xl font-bold mb-2">Conecte o YouTube Analytics</h2>
        <p className="text-[#6b7280] mb-6">Configure a YouTube API Key no backend para começar a receber dados</p>
        <button className="bg-[#7c3aed] hover:bg-[#6d28d9] text-white px-6 py-3 rounded-lg font-medium transition-colors">
          Configurar Integração
        </button>
      </div>
    </div>
  );
}
