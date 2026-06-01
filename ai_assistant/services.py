import requests
from django.conf import settings
from shop.models import Product, Category


def get_store_context():
    categories = Category.objects.all()
    cat_list = ', '.join([c.name for c in categories])
    product_count = Product.objects.filter(is_available=True).count()
    featured = Product.objects.filter(is_featured=True, is_available=True)[:5]
    featured_list = ', '.join([f"{p.name} ({p.final_price:,} so'm)" for p in featured])
    return f"""
Siz "MebelUz" onlayn mebel do'konining AI yordamchisisiz. 
Do'kon haqida:
- Kategoriyalar: {cat_list}
- Jami mavjud mahsulotlar: {product_count} ta
- Tavsiya etilgan mahsulotlar: {featured_list}
- Do'kon Toshkent, O'zbekistonda joylashgan
- Yetkazib berish: butun O'zbekiston bo'ylab
- Ish vaqti: Du-Sha, 9:00-18:00

Faqat o'zbek tilida javob bering. Mebel, uy jihozlari va do'kon haqida yordam bering.
Qisqa, aniq va foydali javoblar bering. Emoji ishlatishingiz mumkin.
"""


def chat_with_ai(messages_history, user_message):
    api_key = settings.OPENROUTER_API_KEY
    model = settings.OPENROUTER_MODEL
    base_url = settings.OPENROUTER_BASE_URL

    if not api_key:
        return "Kechirasiz, AI yordamchi hozir ishlamayapti. Iltimos, keyinroq urinib ko'ring."

    system_prompt = get_store_context()

    api_messages = [{"role": "system", "content": system_prompt}]
    for msg in messages_history[-10:]:
        api_messages.append({"role": msg['role'], "content": msg['content']})
    api_messages.append({"role": "user", "content": user_message})

    try:
        response = requests.post(
            base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://mebeluz.uz",
                "X-Title": "MebelUz AI Assistant",
            },
            json={
                "model": model,
                "messages": api_messages,
                "max_tokens": 500,
                "temperature": 0.7,
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']
    except requests.exceptions.Timeout:
        return "Kechirasiz, so'rov vaqti tugadi. Iltimos, qayta urinib ko'ring."
    except requests.exceptions.RequestException as e:
        return f"Kechirasiz, xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring."
    except (KeyError, IndexError):
        return "Kechirasiz, javob olishda xatolik yuz berdi."
