export type Unit = "adet" | "gram" | "kilo";

export type Product = {
  id: number;
  name: string;
  quantity: number;
  unit: Unit;
  estimatedExpirationDays: number;
  storageAdvice: string;
  createdAt: string;
  daysRemaining: number;
};

export type ProductCreate = {
  name: string;
  quantity: number;
  unit: Unit;
  estimatedExpirationDays?: number;
  storageAdvice?: string;
};

export type AiEntryPreview = {
  productName: string;
  quantityEstimate: number;
  unit: Unit;
  estimatedStorageDays: number;
  storageAdvice: string;
  confidence: number;
};

