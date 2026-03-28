import type { Unit } from "@/lib/types";

export default function CriticalBadge({ daysRemaining }: { daysRemaining: number; unit?: Unit }) {
  if (daysRemaining <= 1) {
    return (
      <span className="inline-flex items-center rounded-full bg-red-600 px-2 py-1 text-xs font-semibold text-white">
        Kritik: {daysRemaining} gün
      </span>
    );
  }

  if (daysRemaining === 2) {
    return (
      <span className="inline-flex items-center rounded-full bg-orange-500 px-2 py-1 text-xs font-semibold text-white">
        Dikkat: {daysRemaining} gün
      </span>
    );
  }

  return (
    <span className="inline-flex items-center rounded-full bg-gray-200 px-2 py-1 text-xs font-semibold text-gray-700">
      {daysRemaining} gün kaldı
    </span>
  );
}

