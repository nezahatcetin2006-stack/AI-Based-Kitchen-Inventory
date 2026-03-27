"use client";

import { useState } from "react";

import type { Product } from "@/lib/types";
import CriticalBadge from "./CriticalBadge";
import { deleteProduct } from "@/lib/api";

type Props = {
  products: Product[];
  onDeleted: () => Promise<void>;
};

export default function ProductList({ products, onDeleted }: Props) {
  const [deletingId, setDeletingId] = useState<number | null>(null);

  async function onDelete(id: number) {
    const ok = window.confirm("Bu ürünü silmek istediğine emin misin?");
    if (!ok) return;

    setDeletingId(id);
    try {
      await deleteProduct(id);
      await onDeleted();
    } catch (e) {
      alert(e instanceof Error ? e.message : "Silme hatası");
    } finally {
      setDeletingId(null);
    }
  }

  if (products.length === 0) {
    return (
      <div className="rounded-lg border border-dashed border-gray-300 bg-white p-6 text-center text-sm text-gray-600">
        Henüz ürün yok. İlk ürünü ekleyin.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {products.map((p) => (
        <div key={p.id} className="rounded-lg border border-gray-200 bg-white p-4">
          <div className="flex items-start justify-between gap-4">
            <div className="min-w-0">
              <div className="truncate text-base font-semibold text-gray-900">{p.name}</div>
              <div className="mt-1 text-sm text-gray-600">
                Miktar: <span className="font-medium">{p.quantity}</span> {p.unit}
              </div>
              <div className="mt-2 text-sm text-gray-700">
                <div className="font-medium text-gray-900">Saklama</div>
                <div className="text-gray-700">{p.storageAdvice}</div>
              </div>
            </div>
            <div className="shrink-0">
              <CriticalBadge daysRemaining={p.daysRemaining} />
              <button
                type="button"
                disabled={deletingId === p.id}
                onClick={() => onDelete(p.id)}
                className="mt-2 w-full rounded-md border border-red-300 bg-white px-2 py-1 text-xs font-semibold text-red-700 disabled:cursor-not-allowed disabled:opacity-70"
              >
                {deletingId === p.id ? "Siliniyor..." : "Sil"}
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

