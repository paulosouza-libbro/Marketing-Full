"use client";

import { useEffect, useState, useRef } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "https://libbro-marketing-production.up.railway.app";

const NOMES: Record<string, string> = {
  cinderela: "Cinderela",
  "joao-e-maria": "João e Maria",
  "o-camponesinho-no-ceu": "O Camponesinho no Céu",
  "chapeuzinho-vermelho": "Chapeuzinho Vermelho",
  "o-pequeno-polegar": "O Pequeno Polegar",
};

const LINK_ICONS: Record<string, string> = {
  youtube: "▶️",
  google_drive: "📁",
  externo: "🔗",
};

export default function Assets() {
  const [contos, setContos] = useState<any[]>([]);
  const [assets, setAssets] = useState<Record<string, any>>({});
  const [uploading, setUploading] = useState<Record<string, boolean>>({});
  const [loading, setLoading] = useState(true);
  const [linkModal, setLinkModal] = useState<{ slug: string; tipo: string; label: string } | null>(null);
  const [linkInput, setLinkInput] = useState("");
  const [linkErro, setLinkErro] = useState("");
  const fileRefs = useRef<Record<string, HTMLInputElement | null>>({});

  const fetchAll = async () => {
    const contosData = await fetch(`${API}/contos`).then(r => r.json()).catch(() => []);
    const lista = Array.isArray(contosData) ? contosData.filter((c: any) => c.slug !== "exemplo-conto") : [];
    setContos(lista);
    const assetsData: Record<string, any> = {};
    await Promise.all(lista.map(async (c: any) => {
      const a = await fetch(`${API}/contos/${c.slug}/assets`).then(r => r.json()).catch(() => null);
      if (a) assetsData[c.slug] = a;
    }));
    setAssets(assetsData);
    setLoading(false);
  };

  useEffect(() => { fetchAll(); }, []);

  const handleUpload = async (slug: string, tipo: string, file: File) => {
    const key = `${slug}-${tipo}`;
    setUploading(prev => ({ ...prev, [key]: true }));
    const form = new FormData();
    form.append("arquivo", file);
    await fetch(`${API}/contos/${slug}/assets/${tipo}`, { method: "POST", body: form });
    await fetchAll();
    setUploading(prev => ({ ...prev, [key]: false }));
  };

  const handleSalvarLink = async () => {
    if (!linkModal) return;
    if (!linkInput.startsWith("http")) {
      setLinkErro("Link inválido — deve começar com https://");
      return;
    }
    setLinkErro("");
    const key = `${linkModal.slug}-${linkModal.tipo}`;
    setUploading(prev => ({ ...prev, [key]: true }));
    await fetch(`${API}/contos/${linkModal.slug}/assets/${linkModal.tipo}/link`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ link: linkInput }),
    });
    setLinkModal(null);
    setLinkInput("");
    await fetchAll();
    setUploading(prev => ({ ...prev, [key]: false }));
  };

  const handleRemover = async (slug: string, tipo: string) => {
    if (!confirm("Remover este asset?")) return;
    await fetch(`${API}/contos/${slug}/assets/${tipo}`, { method: "DELETE" });
    await fetchAll();
  };

  if (loading) return <div className="p-8 text-zinc-500">Carregando assets...</div>;

  return (
    <div className="p-8 max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-1">Assets dos Contos</h1>
        <p className="text-zinc-500">Arquivos entregues pela fábrica — necessários para os agentes executarem campanhas</p>
      </div>

      <div className="space-y-6">
        {contos.map(conto => {
          const assetData = assets[conto.slug];
          if (!assetData) return null;
          const { assets: lista, progresso, completo } = assetData;

          return (
            <div key={conto.slug} className="bg-zinc-900 border border-zinc-800 rounded-2xl overflow-hidden">
              <div className="px-6 py-4 border-b border-zinc-800 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <h2 className="font-semibold text-lg">{NOMES[conto.slug] || conto.nome}</h2>
                  <span className={`text-xs px-2 py-0.5 rounded-full border ${completo ? "bg-emerald-900/40 text-emerald-300 border-emerald-800/40" : "bg-amber-900/40 text-amber-300 border-amber-800/40"}`}>
                    {completo ? "✓ Completo" : `${progresso.preenchidos}/${progresso.total} assets`}
                  </span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-32 h-1.5 bg-zinc-800 rounded-full">
                    <div className={`h-1.5 rounded-full transition-all ${completo ? "bg-emerald-500" : "bg-amber-500"}`} style={{ width: `${progresso.pct}%` }} />
                  </div>
                  <span className="text-xs text-zinc-500">{progresso.pct}%</span>
                </div>
              </div>

              <div className="divide-y divide-zinc-800">
                {lista.map((asset: any) => {
                  const key = `${conto.slug}-${asset.tipo}`;
                  const isUploading = uploading[key];
                  const preenchido = asset.status === "preenchido";

                  return (
                    <div key={asset.tipo} className="px-6 py-4 flex items-center justify-between gap-4">
                      <div className="flex items-center gap-3 min-w-0">
                        <span className="text-xl shrink-0">{asset.icon}</span>
                        <div className="min-w-0">
                          <p className="text-sm font-medium">{asset.label}</p>
                          {preenchido ? (
                            asset.link ? (
                              <a href={asset.link} target="_blank" rel="noopener noreferrer"
                                className="text-xs text-blue-400 hover:text-blue-300 mt-0.5 flex items-center gap-1">
                                {LINK_ICONS[asset.link_tipo] || "🔗"} {asset.link.length > 50 ? asset.link.slice(0, 50) + "..." : asset.link}
                              </a>
                            ) : (
                              <p className="text-xs text-emerald-400 mt-0.5">
                                ✓ {asset.arquivo} · {new Date(asset.enviado_em).toLocaleDateString("pt-BR")}
                              </p>
                            )
                          ) : (
                            <p className="text-xs text-zinc-600 mt-0.5">Pendente — aceita arquivo ou link</p>
                          )}
                        </div>
                      </div>

                      <div className="flex items-center gap-2 shrink-0">
                        {preenchido ? (
                          <>
                            <span className="text-xs bg-emerald-900/30 text-emerald-400 px-2 py-1 rounded-lg">Preenchido</span>
                            <button onClick={() => { setLinkModal({ slug: conto.slug, tipo: asset.tipo, label: asset.label }); setLinkInput(asset.link || ""); }}
                              className="text-xs text-zinc-500 hover:text-zinc-300 px-2 py-1 rounded-lg hover:bg-zinc-800 transition-colors">
                              Editar link
                            </button>
                            <button onClick={() => fileRefs.current[key]?.click()}
                              className="text-xs text-zinc-500 hover:text-zinc-300 px-2 py-1 rounded-lg hover:bg-zinc-800 transition-colors">
                              Trocar arquivo
                            </button>
                            <button onClick={() => handleRemover(conto.slug, asset.tipo)}
                              className="text-xs text-zinc-600 hover:text-red-400 px-2 py-1 rounded-lg hover:bg-zinc-800 transition-colors">✕</button>
                          </>
                        ) : (
                          <>
                            <button
                              onClick={() => { setLinkModal({ slug: conto.slug, tipo: asset.tipo, label: asset.label }); setLinkInput(""); }}
                              disabled={isUploading}
                              className="text-xs bg-zinc-800 hover:bg-zinc-700 disabled:opacity-50 text-white px-3 py-2 rounded-lg transition-colors font-medium"
                            >
                              🔗 Link
                            </button>
                            <button
                              onClick={() => fileRefs.current[key]?.click()}
                              disabled={isUploading}
                              className="text-xs bg-zinc-800 hover:bg-zinc-700 disabled:opacity-50 text-white px-3 py-2 rounded-lg transition-colors font-medium"
                            >
                              {isUploading ? "Enviando..." : "⬆ Arquivo"}
                            </button>
                          </>
                        )}

                        <input type="file" className="hidden"
                          ref={el => { fileRefs.current[key] = el; }}
                          accept={asset.extensoes_aceitas.join(",")}
                          onChange={e => { const f = e.target.files?.[0]; if (f) handleUpload(conto.slug, asset.tipo, f); e.target.value = ""; }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>

      {/* Modal de link */}
      {linkModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-zinc-900 border border-zinc-700 rounded-2xl w-full max-w-md p-6">
            <h2 className="font-bold mb-1">Adicionar link</h2>
            <p className="text-zinc-500 text-sm mb-4">{linkModal.label}</p>
            <input
              type="url"
              placeholder="https://youtube.com/... ou https://drive.google.com/..."
              className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-3 text-sm text-white placeholder-zinc-500 focus:outline-none focus:border-purple-500 mb-2"
              value={linkInput}
              onChange={e => { setLinkInput(e.target.value); setLinkErro(""); }}
              autoFocus
            />
            {linkErro && <p className="text-red-400 text-xs mb-3">{linkErro}</p>}
            <p className="text-zinc-600 text-xs mb-4">Aceita links do YouTube, Google Drive ou qualquer URL pública.</p>
            <div className="flex gap-3">
              <button onClick={() => { setLinkModal(null); setLinkInput(""); setLinkErro(""); }}
                className="flex-1 bg-zinc-800 hover:bg-zinc-700 py-3 rounded-xl text-sm font-medium transition-colors">
                Cancelar
              </button>
              <button onClick={handleSalvarLink} disabled={!linkInput}
                className="flex-1 bg-purple-600 hover:bg-purple-500 disabled:opacity-40 py-3 rounded-xl text-sm font-semibold transition-colors">
                Salvar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
