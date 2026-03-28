"use client";

import { useRef, useState } from "react";
import type { AiEntryPreview, ProductCreate, Unit } from "@/lib/types";
import { analyzeProductImage, createProduct } from "@/lib/api";

const UNITS: Unit[] = ["adet", "gram", "kilo"];
const MAX_IMAGE_BYTES = 4_194_304; // backend: VISION_MAX_IMAGE_BYTES

export default function AiEntryUpload({ onAdded }: { onAdded: () => Promise<void> }) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [preview, setPreview] = useState<AiEntryPreview | null>(null);
  const [draft, setDraft] = useState<AiEntryPreview | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  function validateFile(file: File): string | null {
    if (!file.type || !file.type.startsWith("image/")) return "Sadece image/* türünde dosya yükleyin.";
    if (file.size <= 0) return "Boş dosya yüklenemez.";
    if (file.size > MAX_IMAGE_BYTES) return `Dosya çok büyük (max ${Math.round(MAX_IMAGE_BYTES / 1024 / 1024)} MB).`;
    return null;
  }

  async function onAnalyze() {
    if (!selectedFile) return;
    const fileError = validateFile(selectedFile);
    if (fileError) {
      setError(fileError);
      return;
    }

    setUploading(true);
    setError(null);
    try {
      const res = await analyzeProductImage(selectedFile);
      setPreview(res);
      setDraft(res);
      setSelectedFile(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Bilinmeyen AI hatası");
    } finally {
      setUploading(false);
    }
  }

  async function onConfirm() {
    if (!draft) return;

    const payload: ProductCreate = {
      name: draft.productName.trim(),
      quantity: draft.quantityEstimate,
      unit: draft.unit,
      estimatedExpirationDays: draft.estimatedStorageDays,
      storageAdvice: draft.storageAdvice.trim()
    };

    setUploading(true);
    setError(null);
    try {
      await createProduct(payload);
      await onAdded();
      setPreview(null);
      setDraft(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Ürün eklenemedi");
    } finally {
      setUploading(false);
    }
  }

  function onCancel() {
    setPreview(null);
    setDraft(null);
    setError(null);
  }

  return (
    <div className="space-y-3 rounded-lg border border-gray-200 bg-white p-4">
      <div className="flex items-center justify-between gap-3">
        <div>
          <div className="text-sm font-semibold text-gray-900">Fotoğraftan ürün tanıma</div>
          <div className="text-xs text-gray-600">AI önerisini al, sonra manuel onayla.</div>
        </div>
      </div>

      <div
        className="flex cursor-pointer items-center justify-center rounded-md border-2 border-dashed border-gray-300 p-6 text-sm text-gray-600 hover:border-gray-400"
        onClick={() => {
          fileInputRef.current?.click();
        }}
        onDragOver={(e) => {
          e.preventDefault();
        }}
        onDrop={(e) => {
          e.preventDefault();
          const f = e.dataTransfer.files?.[0];
          if (!f) return;
          const fileError = validateFile(f);
          if (fileError) {
            setError(fileError);
            return;
          }
          setSelectedFile(f);
          setPreview(null);
          setDraft(null);
          setError(null);
        }}
      >
        <div className="text-center">
          <div className="font-medium">Dosya seç veya sürükle-bırak</div>
          <div className="mt-1 text-xs text-gray-500">Maks 4MB • image/*</div>
          <input
            type="file"
            accept="image/*"
            className="hidden"
            ref={fileInputRef}
            onChange={(e) => {
              const f = e.target.files?.[0];
              if (!f) return;
              const fileError = validateFile(f);
              if (fileError) {
                setError(fileError);
                return;
              }
              setSelectedFile(f);
              setPreview(null);
              setDraft(null);
              setError(null);
            }}
          />
        </div>
      </div>

      {selectedFile ? (
        <div className="flex items-center justify-between gap-3 rounded-md bg-gray-50 p-3">
          <div className="min-w-0">
            <div className="truncate text-sm font-medium text-gray-900">{selectedFile.name}</div>
            <div className="text-xs text-gray-600">{Math.round(selectedFile.size / 1024)} KB</div>
          </div>
          <button
            type="button"
            disabled={uploading}
            onClick={onAnalyze}
            className="rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-70"
          >
            {uploading ? "Analiz ediliyor..." : "AI Analiz"}
          </button>
        </div>
      ) : null}

      {preview && draft ? (
        <div className="space-y-3 rounded-lg border border-gray-200 bg-gray-50 p-3">
          <div className="flex items-center justify-between gap-3">
            <div className="text-sm font-semibold text-gray-900">AI Önizleme</div>
            <div className="text-xs text-gray-700">Güven: {(draft.confidence * 100).toFixed(0)}%</div>
          </div>

          <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
            <div className="space-y-1">
              <label className="text-xs font-medium text-gray-700">Ürün adı</label>
              <input
                className="w-full rounded-md border border-gray-300 p-2 text-sm"
                value={draft.productName}
                onChange={(e) => setDraft({ ...draft, productName: e.target.value })}
              />
            </div>
            <div className="space-y-1">
              <label className="text-xs font-medium text-gray-700">Miktar (tahmin)</label>
              <input
                type="number"
                step="0.01"
                className="w-full rounded-md border border-gray-300 p-2 text-sm"
                value={draft.quantityEstimate}
                onChange={(e) => setDraft({ ...draft, quantityEstimate: Number(e.target.value) })}
              />
            </div>
            <div className="space-y-1">
              <label className="text-xs font-medium text-gray-700">Birim</label>
              <select
                className="w-full rounded-md border border-gray-300 p-2 text-sm"
                value={draft.unit}
                onChange={(e) => setDraft({ ...draft, unit: e.target.value as Unit })}
              >
                {UNITS.map((u) => (
                  <option key={u} value={u}>
                    {u}
                  </option>
                ))}
              </select>
            </div>
            <div className="space-y-1">
              <label className="text-xs font-medium text-gray-700">Tahmini gün</label>
              <input
                type="number"
                step="1"
                min={0}
                max={3650}
                className="w-full rounded-md border border-gray-300 p-2 text-sm"
                value={draft.estimatedStorageDays}
                onChange={(e) => setDraft({ ...draft, estimatedStorageDays: Number(e.target.value) })}
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-xs font-medium text-gray-700">Saklama tavsiyesi</label>
            <input
              className="w-full rounded-md border border-gray-300 p-2 text-sm"
              value={draft.storageAdvice}
              onChange={(e) => setDraft({ ...draft, storageAdvice: e.target.value })}
            />
          </div>

          {error ? <div className="rounded bg-red-50 p-2 text-sm text-red-700">{error}</div> : null}

          <div className="flex flex-col gap-2 sm:flex-row sm:justify-end">
            <button
              type="button"
              disabled={uploading}
              onClick={onCancel}
              className="rounded-md border border-gray-300 bg-white px-3 py-2 text-sm font-semibold text-gray-800 disabled:cursor-not-allowed disabled:opacity-70"
            >
              İptal
            </button>
            <button
              type="button"
              disabled={uploading}
              onClick={onConfirm}
              className="rounded-md bg-green-700 px-3 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-70"
            >
              Onayla ve Ekle
            </button>
          </div>
        </div>
      ) : null}

      {error && !preview ? <div className="rounded bg-red-50 p-2 text-sm text-red-700">{error}</div> : null}
    </div>
  );
}

