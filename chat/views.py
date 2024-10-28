from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from transformers import MarianMTModel, MarianTokenizer
from .models import Message  # Import the Message model
import json

# Load translation models once when the server starts
model_en_to_es, tokenizer_en_to_es = None, None
model_es_to_en, tokenizer_es_to_en = None, None

def load_translation_models():
    global model_en_to_es, tokenizer_en_to_es, model_es_to_en, tokenizer_es_to_en
    if not model_en_to_es:
        model_en_to_es, tokenizer_en_to_es = load_translation_model("Helsinki-NLP/opus-mt-en-es")
        model_es_to_en, tokenizer_es_to_en = load_translation_model("Helsinki-NLP/opus-mt-es-en")

def load_translation_model(model_name):
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return model, tokenizer

def translate_text(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

@csrf_exempt
def translate_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        customer_message = data.get("message")
        sender = data.get("sender")

        if not customer_message or not sender:
            return JsonResponse({"error": "Invalid input"}, status=400)

        load_translation_models()

        # Determine the translation direction based on the sender
        if sender == "customer":
            translated_message = translate_text(customer_message, model_es_to_en, tokenizer_es_to_en)
        else:  # sender == "agent"
            translated_message = translate_text(customer_message, model_en_to_es, tokenizer_en_to_es)

        # Save both the original and translated messages in the database
        message = Message.objects.create(
            sender=sender,
            content=customer_message,
            translated_content=translated_message
        )

        return JsonResponse({"translated_message": translated_message, "message_id": message.id})

    return JsonResponse({"error": "Invalid request method"}, status=405)


def get_messages(request):
    messages = Message.objects.all().order_by('timestamp')  # Fetch all messages sorted by time
    message_data = [
        {
            "id": msg.id,
            "sender": msg.sender,
            "content": msg.content,
            "translated_content": msg.translated_content,
            "timestamp": msg.timestamp
        }
        for msg in messages
    ]
    return JsonResponse(message_data, safe=False)