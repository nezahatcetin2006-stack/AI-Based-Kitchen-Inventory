"use client";

import { useEffect, useState } from "react";
import AddProductForm from "@/components/AddProductForm";
import AiEntryUpload from "@/components/AiEntryUpload";
import ProductList from "@/components/ProductList";
import RecipeSuggestionPanel from "@/components/RecipeSuggestionPanel";
import type { Product } from "@/lib/types";
import { fetchProducts } from "@/lib/api";

export default function HomePage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchProducts();
      setProducts(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Bilinmeyen hata");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <main className="mx-auto max-w-3xl space-y-6 p-6">
      <header className="space-y-2">
        <h1 className="text-2xl font-bold">Mutfak Envanteri</h1>
        <p className="text-sm text-gray-600">Son tüketim yaklaşan ürünleri kritik renklerle vurgular.</p>
      </header>

      <section className="space-y-3">
        <AddProductForm onAdded={load} />
        <AiEntryUpload onAdded={load} />
        <RecipeSuggestionPanel />
        <div className="rounded-lg border border-gray-200 bg-white p-4 text-sm text-gray-600">
          Manuel ekleme: `kalan tahmini gün` ve `saklama tavsiyesi` AI tarafından otomatik doldurulur.
        </div>
      </section>

      <section className="space-y-3">
        <h2 className="text-lg font-semibold">Ürünler</h2>
        {loading ? (
          <div className="rounded-lg border border-gray-200 bg-white p-6 text-center text-sm text-gray-600">
            Yükleniyor...
          </div>
        ) : error ? (
          <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-800">{error}</div>
        ) : (
          <ProductList products={products} onDeleted={load} />
        )}
      </section>
    </main>
  );
}

