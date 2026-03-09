const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchAPI(path: string, options?: RequestInit) {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

// Campanhas
export const getCampanhas = () => fetchAPI("/campanhas");
export const createCampanha = (body: { briefing: string; conto: string; canais: string[] }) =>
  fetchAPI("/campanhas", { method: "POST", body: JSON.stringify(body) });
export const getCampanha = (id: string) => fetchAPI(`/campanhas/${id}`);

// Aprovações
export const getAprovacoes = () => fetchAPI("/aprovacoes");
export const aprovar = (id: string, action: "approve" | "reject", feedback?: string) =>
  fetchAPI(`/aprovacoes/${id}`, { method: "POST", body: JSON.stringify({ action, feedback }) });

// Contos
export const getContos = () => fetchAPI("/contos");
export const getConto = (slug: string) => fetchAPI(`/contos/${slug}`);
export const createConto = (body: { slug: string; nome: string; estilo: string }) =>
  fetchAPI("/contos", { method: "POST", body: JSON.stringify(body) });

// Agentes
export const getAgentes = () => fetchAPI("/agentes");
