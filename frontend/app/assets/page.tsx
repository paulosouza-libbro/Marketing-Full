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

export default function Assets() {
  const [contos, setContos] = useState<any[]>([]);
  const [assets, setAssets] = useState<Record<string, any>>({});
  const [uploading, setUploading] = useState<Record<string, boolean>>({});
  const [loading, setLoading] = useState(true);
  const fileRefs = useRef<Record<string, HTMLInputElement | null>>({});

  const fetchAll = async () => {
    const contosData = await fetch(`${API}/contos`).then(r => r.json()).catch(() => []);
    const lista = Array.isArray(contosData) ? contosData.filter(c => c.slug !== "exemplo-conto") : [];
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

  const handleRemover = async (slug: string, tipo: string) => {
    if (!confirm("Remover este asset?")) return;
    await fetch(`${API}/contos/${slug}/assets/${tipo}`, { method: "DELETE" });
    await fetchAll();
  };

  if (loading) return (
    <div className="p-8 max-w-7xl mx-auto text-zinc-500">Carregando assets...</div>
  );

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
              {/* Header do conto */}
              <div className="px-6 py-4 border-b border-zinc-800 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <h2 className="font-semibold text-lg">{NOMES[conto.slug] || conto.nome}</h2>
                  {completo ? (
                    <span className="text-xs bg-emerald-900/40 text-emerald-300 px-2 py-0.5 rounded-full border border-emerald-800/40">
                      ✓ Completo
                    </span>
                  ) : (
                    <span className="text-xs bg-amber-900/40 text-amber-300 px-2 py-0.5 rounded-full border border-amber-800/40">
                      {progresso.preenchidos}/{progresso.total} assets
                    </span>
                  )}
                </div>
                {/* Barra de progresso */}
                <div className="flex items-center gap-3">
                  <div className="w-32 h-1.5 bg-zinc-800 rounded-full">
                    <div
                      className={`h-1.5 rounded-full transition-all ${completo ? "bg-emerald-500" : "bg-amber-500"}`}
                      style={{ width: `${progresso.pct}%` }}
                    />
                  </div>
                  <span className="text-xs text-zinc-500">{progresso.pct}%</span>
                </div>
              </div>

              {/* Lista de assets */}
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
                            <p className="text-xs text-emerald-400 mt-0.5">
                              ✓ {asset.arquivo} · {new Date(asset.enviado_em).toLocaleDateString("pt-BR")}
                            </p>
                          ) : (
                            <p className="text-xs text-zinc-600 mt-0.5">
                              Aceita: {asset.extensoes_aceitas.join(", ")}
                            </p>
                          )}
                        </div>
                      </div>

                      <div className="flex items-center gap-2 shrink-0">
                        {preenchido ? (
                          <>
                            <span className="text-xs bg-emerald-900/30 text-emerald-400 px-2 py-1 rounded-lg">
                              Preenchido
                            </span>
                            <button
                              onClick={() => fileRefs.current[key]?.click()}
                              className="text-xs text-zinc-500 hover:text-zinc-300 px-2 py-1 rounded-lg hover:bg-zinc-800 transition-colors"
                            >
                              Substituir
                            </button>
                            <button
                              onClick={() => handleRemover(conto.slug, asset.tipo)}
                              className="text-xs text-zinc-600 hover:text-red-400 px-2 py-1 rounded-lg hover:bg-zinc-800 transition-colors"
                            >
                              ✕
                            </button>
                          </>
                        ) : (
                          <button
                            onClick={() => fileRefs.current[key]?.click()}
                            disabled={isUploading}
                            className="text-xs bg-zinc-800 hover:bg-zinc-700 disabled:opacity-50 text-white px-4 py-2 rounded-lg transition-colors font-medium"
                          >
                            {isUploading ? "Enviando..." : "⬆ Upload"}
                          </button>
                        )}

                        {/* Input oculto */}
                        <input
                          type="file"
                          className="hidden"
                          ref={el => { fileRefs.current[key] = el; }}
                          accept={asset.extensoes_aceitas.join(",")}
                          onChange={e => {
                            const file = e.target.files?.[0];
                            if (file) handleUpload(conto.slug, asset.tipo, file);
                            e.target.value = "";
                          }}
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
    </div>
  );
}
