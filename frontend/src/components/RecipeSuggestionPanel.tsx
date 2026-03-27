"use client";

import { useState } from "react";

import { getRecipeSuggestions } from "@/lib/api";
import type { RecipeSuggestion } from "@/lib/types";

export default function RecipeSuggestionPanel() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [recipes, setRecipes] = useState<RecipeSuggestion[]>([]);

  async function onGetSuggestions() {
    setLoading(true);
    setError(null);
    try {
      const res = await getRecipeSuggestions();
      setRecipes(res.recipes ?? []);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Tarif önerisi alınamadı");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="space-y-3 rounded-lg border border-gray-200 bg-white p-4">
      <div className="flex items-center justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold">AI Şef</h2>
          <p className="text-sm text-gray-600">Tarihi yaklaşan ürünleri öncelikleyerek tarif önerir.</p>
        </div>
        <button
          type="button"
          onClick={onGetSuggestions}
          disabled={loading}
          className="rounded-md bg-emerald-600 px-3 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-70"
        >
          {loading ? "Öneri hazırlanıyor..." : "Tarif Önerisi Al"}
        </button>
      </div>

      {error ? <div className="rounded bg-red-50 p-2 text-sm text-red-700">{error}</div> : null}

      {recipes.length > 0 ? (
        <div className="space-y-3">
          {recipes.map((recipe, idx) => (
            <article key={`${recipe.recipeTitle}-${idx}`} className="rounded-md border border-gray-200 bg-gray-50 p-3">
              <div className="text-base font-semibold text-gray-900">{recipe.recipeTitle}</div>
              {recipe.focusProducts?.length ? (
                <div className="mt-1 text-xs text-amber-700">Oncelikli urunler: {recipe.focusProducts.join(", ")}</div>
              ) : null}
              <div className="mt-2 text-sm text-gray-800">
                <div className="font-medium">Malzemeler</div>
                <ul className="ml-5 list-disc">
                  {recipe.ingredients.map((item, i) => (
                    <li key={`${idx}-ing-${i}`}>{item}</li>
                  ))}
                </ul>
              </div>
              <div className="mt-2 text-sm text-gray-800">
                <div className="font-medium">Adımlar</div>
                <ol className="ml-5 list-decimal">
                  {recipe.steps.map((step, i) => (
                    <li key={`${idx}-step-${i}`}>{step}</li>
                  ))}
                </ol>
              </div>
              <div className="mt-2 text-xs text-gray-600">
                {recipe.servings ? `Porsiyon: ${recipe.servings}` : ""} {recipe.calories ? `• Kalori: ${recipe.calories}` : ""}
              </div>
              {recipe.note ? <div className="mt-2 text-xs text-gray-700">{recipe.note}</div> : null}
            </article>
          ))}
        </div>
      ) : (
        <div className="text-sm text-gray-600">Henüz öneri yok. Butona tıklayıp tarif üretin.</div>
      )}
    </section>
  );
}

