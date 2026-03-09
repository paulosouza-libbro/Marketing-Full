import Link from "next/link";

const campanhas: never[] = [];

export default function Campanhas() {
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold mb-1">Campanhas</h1>
          <p className="text-[#6b7280]">Histórico e status de todas as campanhas</p>
        </div>
        <Link
          href="/campanhas/nova"
          className="bg-[#7c3aed] hover:bg-[#6d28d9] text-white px-5 py-2.5 rounded-lg font-medium transition-colors"
        >
          + Nova Campanha
        </Link>
      </div>

      {campanhas.length === 0 ? (
        <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl p-16 text-center">
          <div className="text-5xl mb-4">🚀</div>
          <h2 className="text-xl font-bold mb-2">Nenhuma campanha ainda</h2>
          <p className="text-[#6b7280] mb-6">Crie sua primeira campanha e deixe os agentes trabalharem</p>
          <Link
            href="/campanhas/nova"
            className="bg-[#7c3aed] hover:bg-[#6d28d9] text-white px-6 py-3 rounded-lg font-medium transition-colors inline-block"
          >
            Criar Primeira Campanha
          </Link>
        </div>
      ) : null}
    </div>
  );
}
