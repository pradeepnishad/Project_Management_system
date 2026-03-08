from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from .models import GrammarCache
import torch

MODEL_NAME = "vennify/t5-base-grammar-correction"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def correct_grammar(text):

    # 1️⃣ Check cache first
    cached = GrammarCache.objects.filter(original_text=text).first()
    if cached:
        return cached.corrected_text

    try:
        input_text = "grammar: " + text

        input_ids = tokenizer.encode(
            input_text,
            return_tensors="pt",
            max_length=512,
            truncation=True
        )

        outputs = model.generate(
            input_ids,
            max_length=512,
            num_beams=4,
            early_stopping=True
        )

        corrected_text = tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        # 2️⃣ Save to cache
        GrammarCache.objects.create(
            original_text=text,
            corrected_text=corrected_text
        )

        return corrected_text

    except Exception as e:
        print("HF Grammar Error:", e)
        return text