export default function Aprovacoes() {
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-1">Aprovações</h1>
        <p className="text-[#6b7280]">Revise e aprove o conteúdo antes de publicar</p>
      </div>

      <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl p-16 text-center">
        <div className="text-5xl mb-4">✅</div>
        <h2 className="text-xl font-bold mb-2">Nada para aprovar</h2>
        <p className="text-[#6b7280]">Quando os agentes gerarem conteúdo, ele aparecerá aqui para sua revisão</p>
      </div>
    </div>
  );
}
