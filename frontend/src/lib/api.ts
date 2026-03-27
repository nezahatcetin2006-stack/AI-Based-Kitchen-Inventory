import type { AiEntryPreview, Product, ProductCreate } from "./types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, "") ?? "http://localhost:8000";

export async function fetchProducts(): Promise<Product[]> {
  const res = await fetch(`${API_BASE_URL}/products`, {
    method: "GET",
    headers: { "Content-Type": "application/json" }
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Ürünler alınamadı (${res.status}): ${text || "Hata"}`);
  }

  return (await res.json()) as Product[];
}

export async function createProduct(payload: ProductCreate): Promise<Product> {
  const res = await fetch(`${API_BASE_URL}/products`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Ürün eklenemedi (${res.status}): ${text || "Hata"}`);
  }

  return (await res.json()) as Product;
}

export async function deleteProduct(id: number): Promise<void> {
  const res = await fetch(`${API_BASE_URL}/products/${id}`, {
    method: "DELETE"
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Ürün silinemedi (${res.status}): ${text || "Hata"}`);
  }
}

export async function analyzeProductImage(file: File): Promise<AiEntryPreview> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE_URL}/products/ai-entry`, {
    method: "POST",
    body: formData
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`AI analiz başarısız (${res.status}): ${text || "Hata"}`);
  }

  return (await res.json()) as AiEntryPreview;
}

