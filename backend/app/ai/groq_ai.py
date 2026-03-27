import asyncio
import base64
import json
from typing import Any

from fastapi import HTTPException
from groq import Groq

from app.config import settings
from app.schemas.ai_entry import AiEntryPreview
from app.schemas.recipe import RecipeSuggestion, RecipeSuggestionResponse


def _extract_json_object(text: str) -> Any:
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("JSON response bulunamadı")

    return json.loads(text[start:end + 1])


def _normalize_unit_and_confidence(parsed: dict[str, Any]) -> dict[str, Any]:

    qty = parsed.get("quantityEstimate")
    if qty is not None:
        try:
            parsed["quantityEstimate"] = float(qty)
        except Exception:
            pass

    days = parsed.get("estimatedStorageDays")
    if days is not None:
        try:
            parsed["estimatedStorageDays"] = int(days)
        except Exception:
            pass

    unit_raw = parsed.get("unit")
    if unit_raw is not None:

        unit_str = str(unit_raw).strip().lower()

        if unit_str in {"adet", "piece", "parca", "parça"}:
            parsed["unit"] = "adet"

        elif unit_str in {"gram", "g"}:
            parsed["unit"] = "gram"

        elif unit_str in {"kilo", "kg", "kilogram"}:
            parsed["unit"] = "kilo"

    conf = parsed.get("confidence")

    if conf is not None:
        try:
            conf_num = float(conf)

            if conf_num > 1:
                conf_num = conf_num / 100.0

            parsed["confidence"] = conf_num

        except Exception:
            parsed["confidence"] = 0.5

    storage = parsed.get("storageAdvice")

    if isinstance(storage, str) and not storage.strip():
        parsed["storageAdvice"] = "Saklama tavsiyesini etikette belirtildiği şekilde uygulayın."

    return parsed


async def analyze_product_image(*, image_bytes: bytes, mime_type: str) -> AiEntryPreview:

    if not settings.GROQ_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="Groq API anahtarı tanımlı değil (`GROQ_API_KEY`).",
        )

    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    data_url = f"data:{mime_type};base64,{image_b64}"

    prompt = (
        "Aşağıdaki mutfak fotoğrafındaki ürünü analiz et ve SADECE JSON döndür.\n"
        "Başlık, açıklama veya markdown kullanma.\n"
        "\n"
        "JSON formatı:\n"
        "{\n"
        '  "productName": "ürün adı",\n'
        '  "quantityEstimate": sayı,\n'
        '  "unit": "adet | gram | kilo",\n'
        '  "estimatedStorageDays": sayı,\n'
        '  "storageAdvice": "saklama tavsiyesi",\n'
        '  "confidence": 0-1\n'
        "}\n"
        "\n"
        "Kurallar:\n"
        "- unit sadece adet, gram veya kilo olabilir\n"
        "- confidence 0 ile 1 arasında olmalı\n"
        "- JSON dışında hiçbir şey yazma\n"
    )

    client = Groq(api_key=settings.GROQ_API_KEY)

    try:

        completion = await asyncio.to_thread(
            client.chat.completions.create,
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": data_url}},
                    ],
                }
            ],
            temperature=0,
            max_tokens=600,
        )

    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Groq API hatası: {e}")

    raw_text = ""

    if completion.choices:
        raw_text = completion.choices[0].message.content

    if not raw_text or not raw_text.strip():
        raise HTTPException(status_code=502, detail="Groq boş yanıt döndürdü")

    try:

        parsed = _extract_json_object(raw_text)

        if not isinstance(parsed, dict):
            raise ValueError("JSON object değil")

        parsed = _normalize_unit_and_confidence(parsed)

        return AiEntryPreview.model_validate(parsed)

    except Exception as e:

        raise HTTPException(
            status_code=502,
            detail=f"Groq JSON parse edilemedi: {e}",
        )


async def analyze_product_text(*, product_name: str, quantity: float, unit: str) -> AiEntryPreview:
    """
    Manuel ürün ekleme için: kullanıcı sadece ad/miktar/birim gönderir.
    Groq'tan metin tabanlı tahmin alır:
    - estimatedStorageDays
    - storageAdvice
    - (aynı şemaya uyacak şekilde) confidence ve unit
    """
    if not settings.GROQ_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="Groq API anahtarı tanımlı değil (`GROQ_API_KEY`).",
        )

    unit_norm = str(unit).strip().lower()
    if unit_norm not in {"adet", "gram", "kilo"}:
        unit_norm = "adet"

    prompt = (
        "Aşağıdaki mutfak ürünü için YALNIZCA JSON döndür.\n"
        "Başlık/markdown/açıklama yazma.\n"
        "JSON şeması:\n"
        "{\n"
        '  "productName": ürün adı,\n'
        '  "quantityEstimate": miktar tahmini (float),\n'
        '  "unit": "adet" | "gram" | "kilo",\n'
        '  "estimatedStorageDays": integer (0-3650),\n'
        '  "storageAdvice": Türkçe kısa saklama tavsiyesi (1-3 cümle),\n'
        '  "confidence": 0-1 arası float\n'
        "}\n\n"
        "Girdi:\n"
        f"- productName: {product_name}\n"
        f"- quantity: {quantity}\n"
        f"- unit: {unit_norm}\n\n"
        "Kurallar:\n"
        "- productName alanı GİRDİDEKİ ürün adıyla aynı olsun.\n"
        "- quantityEstimate alanında quantity değerini float olarak aynen kullan.\n"
        "- unit alanı mutlaka unit alanıyla aynı ('adet'|'gram'|'kilo').\n"
        "- estimatedStorageDays düşük güven durumunda bile makul bir tahmin olsun.\n"
    )

    client = Groq(api_key=settings.GROQ_API_KEY)

    try:
        completion = await asyncio.to_thread(
            client.chat.completions.create,
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}],
                }
            ],
            temperature=0,
            max_completion_tokens=600,
            stream=False,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Groq API hatası: {e}") from e

    raw_text = completion.choices[0].message.content if completion.choices else ""
    if not raw_text or not raw_text.strip():
        raise HTTPException(status_code=502, detail="Groq boş yanıt döndürdü")

    try:
        parsed = _extract_json_object(raw_text)
        if not isinstance(parsed, dict):
            raise ValueError("JSON object değil")
        parsed = _normalize_unit_and_confidence(parsed)
        return AiEntryPreview.model_validate(parsed)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Groq JSON parse edilemedi: {e}") from e


async def generate_recipe_suggestions_from_inventory(
    *,
    inventory_rows: list[dict[str, Any]],
) -> RecipeSuggestionResponse:
    """
    Envanter girdisine göre (özellikle günü az kalan ürünleri öncelikleyerek) tarif önerileri üretir.
    """
    if not settings.GROQ_API_KEY:
        raise HTTPException(status_code=503, detail="Groq API anahtarı tanımlı değil (`GROQ_API_KEY`).")

    if not inventory_rows:
        return RecipeSuggestionResponse(
            recipes=[
                RecipeSuggestion(
                    recipeTitle="Envanter Boş",
                    ingredients=[],
                    steps=["Önce envantere birkaç ürün ekleyin, sonra tekrar tarif önerisi alın."],
                    note="Tarif üretmek için envanterde ürün olmalı.",
                )
            ]
        )

    inv_json = json.dumps(inventory_rows, ensure_ascii=False)
    prompt = (
        "Sen bir mutfak asistanısın. Verilen envantere göre kullanımı kolay tarif önerileri üret.\n"
        "ÖNCELİK: daysRemaining değeri düşük olan ürünleri önce değerlendir.\n"
        "Sadece JSON döndür. Ek açıklama yazma.\n"
        "JSON şeması:\n"
        "{\n"
        '  "recipes": [\n'
        "    {\n"
        '      "recipeTitle": "string",\n'
        '      "ingredients": ["string"],\n'
        '      "steps": ["string"],\n'
        '      "servings": number | null,\n'
        '      "calories": number | null,\n'
        '      "focusProducts": ["string"],\n'
        '      "note": "string"\n'
        "    }\n"
        "  ]\n"
        "}\n\n"
        "Kurallar:\n"
        "- 1 ile 3 arası tarif öner.\n"
        "- focusProducts alanına özellikle tarihi yakın ürünleri koy.\n"
        "- Tarifler pratik ve gerçek hayatta uygulanabilir olsun.\n"
        "- Dil Türkçe olsun.\n\n"
        f"Envanter: {inv_json}"
    )

    client = Groq(api_key=settings.GROQ_API_KEY)
    completion = await asyncio.to_thread(
        client.chat.completions.create,
        model=settings.GROQ_MODEL,
        messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
        temperature=0.4,
        max_completion_tokens=1200,
        stream=False,
    )

    raw_text = completion.choices[0].message.content if completion.choices else ""
    if not raw_text or not raw_text.strip():
        raise HTTPException(status_code=502, detail="Groq tarif önerisi için boş yanıt döndürdü.")

    try:
        parsed = _extract_json_object(raw_text)
        if not isinstance(parsed, dict):
            raise ValueError("JSON object değil")
        return RecipeSuggestionResponse.model_validate(parsed)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Groq tarif JSON parse edilemedi: {e}") from e

