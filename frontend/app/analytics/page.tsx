"use client";

import { useEffect, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "https://libbro-marketing-production.up.railway.app";

export default function Analytics() {
  const [meta, setMeta] = useState<any>(null);
  const [postsFB, setPostsFB] = useState<any[]>([]);
  const [postsIG, setPostsIG] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch(`${API}/meta/status`).then(r => r.json()).catch(() => null),
      fetch(`${API}/meta/facebook/posts?limit=5`).then(r => r.json()).catch(() => ({ data: [] })),
      fetch(`${API}/meta/instagram/posts?limit=5`).then(r => r.json()).catch(() => ({ data: [] })),
    ]).then(([status, fb, ig]) => {
      setMeta(status);
      setPostsFB(fb?.data || []);
      setPostsIG(ig?.data || []);
      setLoading(false);
    });
  }, []);

  if (loading) return <div className="p-8 text-zinc-500">Carregando analytics...</div>;

  return (
    <div className="p-8 max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-1">Analytics</h1>
        <p className="text-zinc-500">Performance da Libbro nas redes sociais</p>
      </div>

      {/* Status Meta */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        {/* Facebook */}
        <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-5">
          <div className="flex items-center gap-2 mb-4">
            <span className="text-xl">👥</span>
            <h2 className="font-semibold">Facebook</h2>
            <span className={`ml-auto text-xs px-2 py-0.5 rounded-full ${meta?.facebook?.seguidores > 0 ? "bg-emerald-900/40 text-emerald-300" : "bg-zinc-800 text-zinc-500"}`}>
              {meta?.facebook?.pagina || "—"}
            </span>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-zinc-800/50 rounded-xl p-3">
              <p className="text-2xl font-bold text-white">{meta?.facebook?.seguidores?.toLocaleString("pt-BR") || "0"}</p>
              <p className="text-xs text-zinc-500 mt-0.5">Seguidores</p>
            </div>
            <div className="bg-zinc-800/50 rounded-xl p-3">
              <p className="text-2xl font-bold text-white">{postsFB.length}</p>
              <p className="text-xs text-zinc-500 mt-0.5">Posts recentes</p>
            </div>
          </div>
        </div>

        {/* Instagram */}
        <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-5">
          <div className="flex items-center gap-2 mb-4">
            <span className="text-xl">📸</span>
            <h2 className="font-semibold">Instagram</h2>
            <span className={`ml-auto text-xs px-2 py-0.5 rounded-full ${meta?.instagram?.conectado ? "bg-emerald-900/40 text-emerald-300" : "bg-amber-900/40 text-amber-300"}`}>
              {meta?.instagram?.conectado ? "Conectado" : "Não conectado"}
            </span>
          </div>
          {meta?.instagram?.conectado ? (
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-zinc-800/50 rounded-xl p-3">
                <p className="text-2xl font-bold text-white">{postsIG.length}</p>
                <p className="text-xs text-zinc-500 mt-0.5">Posts recentes</p>
              </div>
              <div className="bg-zinc-800/50 rounded-xl p-3">
                <p className="text-2xl font-bold text-white">
                  {postsIG.reduce((acc: number, p: any) => acc + (p.like_count || 0), 0)}
                </p>
                <p className="text-xs text-zinc-500 mt-0.5">Curtidas totais</p>
              </div>
            </div>
          ) : (
            <p className="text-zinc-600 text-sm">Conecte o Instagram à página do Facebook para ver os dados.</p>
          )}
        </div>
      </div>

      {/* Posts Facebook */}
      {postsFB.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold mb-4">Posts recentes — Facebook</h2>
          <div className="space-y-3">
            {postsFB.map((post: any) => (
              <div key={post.id} className="bg-zinc-900 border border-zinc-800 rounded-xl p-4 flex items-start justify-between gap-4">
                <div className="min-w-0">
                  <p className="text-sm text-zinc-300 line-clamp-2">{post.message || "(sem texto)"}</p>
                  <p className="text-xs text-zinc-600 mt-1">{new Date(post.created_time).toLocaleDateString("pt-BR")}</p>
                </div>
                <div className="flex gap-4 shrink-0 text-center">
                  <div>
                    <p className="text-sm font-semibold">{post.likes?.summary?.total_count || 0}</p>
                    <p className="text-xs text-zinc-600">❤️</p>
                  </div>
                  <div>
                    <p className="text-sm font-semibold">{post.comments?.summary?.total_count || 0}</p>
                    <p className="text-xs text-zinc-600">💬</p>
                  </div>
                  <div>
                    <p className="text-sm font-semibold">{post.shares?.count || 0}</p>
                    <p className="text-xs text-zinc-600">🔁</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Posts Instagram */}
      {postsIG.length > 0 && (
        <div>
          <h2 className="text-lg font-semibold mb-4">Posts recentes — Instagram</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {postsIG.map((post: any) => (
              <div key={post.id} className="bg-zinc-900 border border-zinc-800 rounded-xl p-4">
                <p className="text-sm text-zinc-300 line-clamp-2 mb-3">{post.caption || "(sem legenda)"}</p>
                <div className="flex gap-4">
                  <div className="text-center">
                    <p className="text-sm font-semibold">{post.like_count || 0}</p>
                    <p className="text-xs text-zinc-600">❤️ Curtidas</p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm font-semibold">{post.comments_count || 0}</p>
                    <p className="text-xs text-zinc-600">💬 Comentários</p>
                  </div>
                  {post.reach && (
                    <div className="text-center">
                      <p className="text-sm font-semibold">{post.reach}</p>
                      <p className="text-xs text-zinc-600">👁️ Alcance</p>
                    </div>
                  )}
                </div>
                <p className="text-xs text-zinc-600 mt-2">{new Date(post.timestamp).toLocaleDateString("pt-BR")}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Vazio */}
      {postsFB.length === 0 && postsIG.length === 0 && (
        <div className="text-center py-16 border border-dashed border-zinc-800 rounded-2xl">
          <p className="text-zinc-500 text-lg mb-2">Nenhum dado disponível ainda</p>
          <p className="text-zinc-600 text-sm">Publique conteúdo nas redes sociais para ver os analytics aqui.</p>
        </div>
      )}
    </div>
  );
}
