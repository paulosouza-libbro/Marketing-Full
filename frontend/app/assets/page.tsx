export default function Assets() {
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-1">Brand Assets</h1>
        <p className="text-[#6b7280]">Referências visuais, identidade de marca e ilustrações dos contos</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

        {/* Identidade Visual */}
        <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl p-6 hover:border-[#7c3aed]/50 transition-colors cursor-pointer">
          <div className="text-3xl mb-3">🎨</div>
          <h3 className="font-bold mb-1">Identidade Visual</h3>
          <p className="text-sm text-[#6b7280] mb-4">Logo, paleta de cores, tipografia e guia de marca</p>
          <div className="text-xs text-[#7c3aed]">Configurar →</div>
        </div>

        {/* Referências Visuais */}
        <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl p-6 hover:border-[#7c3aed]/50 transition-colors cursor-pointer">
          <div className="text-3xl mb-3">🖼️</div>
          <h3 className="font-bold mb-1">Referências Visuais</h3>
          <p className="text-sm text-[#6b7280] mb-4">Moodboards, inspirações e referências de estilo geral</p>
          <div className="text-xs text-[#7c3aed]">Ver referências →</div>
        </div>

        {/* Contos */}
        <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl p-6 hover:border-[#7c3aed]/50 transition-colors cursor-pointer">
          <div className="text-3xl mb-3">📖</div>
          <h3 className="font-bold mb-1">Ilustrações dos Contos</h3>
          <p className="text-sm text-[#6b7280] mb-4">Referências visuais por conto — estilo, personagens e cenários</p>
          <div className="text-xs text-[#7c3aed]">Gerenciar contos →</div>
        </div>
      </div>

      {/* Upload Area */}
      <div className="mt-6 bg-[#1a1a1a] border-2 border-dashed border-[#2a2a2a] rounded-xl p-12 text-center hover:border-[#7c3aed]/50 transition-colors cursor-pointer">
        <div className="text-4xl mb-3">⬆️</div>
        <h3 className="font-bold mb-1">Fazer Upload de Referências</h3>
        <p className="text-sm text-[#6b7280]">Arraste arquivos ou clique para selecionar — PNG, JPG, SVG</p>
      </div>
    </div>
  );
}
