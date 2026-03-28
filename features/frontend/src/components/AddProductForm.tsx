"use client";

import { useState } from "react";
import type { FormEvent } from "react";
import type { ProductCreate, Unit } from "@/lib/types";
import { createProduct } from "@/lib/api";

const UNITS: Unit[] = ["adet", "gram", "kilo"];

type Props = {
  onAdded: () => Promise<void>;
};

export default function AddProductForm({ onAdded }: Props) {
  const [name, setName] = useState("");
  const [quantity, setQuantity] = useState<string>("1");
  const [unit, setUnit] = useState<Unit>("adet");

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);

    const trimmedName = name.trim();
    const qty = Number(quantity);

    if (!trimmedName) return setError("Ürün adı gerekli.");
    if (!Number.isFinite(qty) || qty < 0 || qty > 100000) return setError("Miktar 0 ile 100000 aralığında olmalı.");

    const payload: ProductCreate = {
      name: trimmedName,
      quantity: qty,
      unit
    };

    try {
      setSubmitting(true);
      await createProduct(payload);
      setName("");
      setQuantity("1");
      setUnit("adet");
      await onAdded();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Bilinmeyen hata");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={onSubmit} className="space-y-4 rounded-lg border border-gray-200 bg-white p-4">
      <div className="space-y-1">
        <label className="text-sm font-medium text-gray-700">Ürün adı</label>
        <input
          className="w-full rounded-md border border-gray-300 p-2"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Örn: Yoğurt"
        />
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="space-y-1">
          <label className="text-sm font-medium text-gray-700">Miktar</label>
          <input
            className="w-full rounded-md border border-gray-300 p-2"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            inputMode="decimal"
          />
        </div>
        <div className="space-y-1">
          <label className="text-sm font-medium text-gray-700">Birim</label>
          <select
            className="w-full rounded-md border border-gray-300 p-2"
            value={unit}
            onChange={(e) => setUnit(e.target.value as Unit)}
          >
            {UNITS.map((u) => (
              <option key={u} value={u}>
                {u}
              </option>
            ))}
          </select>
        </div>
      </div>

      {error ? <div className="rounded bg-red-50 p-2 text-sm text-red-700">{error}</div> : null}

      <button
        type="submit"
        disabled={submitting}
        className="w-full rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-70"
      >
        {submitting ? "Ekleniyor..." : "Ürün Ekle"}
      </button>
    </form>
  );
}

