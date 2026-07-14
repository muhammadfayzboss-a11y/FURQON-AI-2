"""
FURQON AI - AI Handler
OpenRouter orqali AI bilan ishlash (BEPUL!)
"""

import json
import re
import requests
from typing import Dict, List
from config import OPENROUTER_API_KEY, AI_BASE_URL, AI_MODEL, AI_FALLBACK_MODELS, AI_MAX_TOKENS, AI_TEMPERATURE
from search_engine import SearchEngine


class AIHandler:
    """AI yordamida savollarga javob berish"""

    def __init__(self):
        self.search = SearchEngine()
        self.api_key = OPENROUTER_API_KEY
        self.base_url = AI_BASE_URL
        self.model = AI_MODEL
        self.fallback_models = AI_FALLBACK_MODELS
        self.all_models = [self.model] + self.fallback_models
        print(f"✅ AI Handler tayyor! Model: {self.model}")

    def _clean_response(self, text: str) -> str:
        """
        AI javobidan thinking/reasoning qismlarini tozalash
        """
        if not text:
            return text

        # <think>...</think> teglarini olib tashlash
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)

        # <thinking>...</thinking> teglarini olib tashlash
        text = re.sub(r'<thinking>.*?</thinking>', '', text, flags=re.DOTALL)

        # "Let me think..." kabi boshlanishlarni olib tashlash
        thinking_patterns = [
            r'^(?:Okay|Let me|Let\'s|I need to|We need to|First|Hmm|Actually|Wait).*?\n\n',
            r'^.*?[Ww]e need to answer.*?\n\n',
            r'^.*?The question.*?means.*?\n\n',
        ]
        for pattern in thinking_patterns:
            text = re.sub(pattern, '', text, flags=re.DOTALL)

        # Bo'sh qatorlarni tozalash
        text = text.strip()

        # Agar javob hali ham thinkingga o'xshasa — faqat oxirgi strukturaviy qismini olish
        if '🕌' not in text and '📖' not in text and len(text) > 500:
            # Oxirgi mantiqiy qismini topishga urinish
            parts = text.split('\n\n')
            for i, part in enumerate(parts):
                if any(kw in part for kw in ['🕌', '📖', '📚', '💡', 'Javob', 'Xulosa']):
                    text = '\n\n'.join(parts[i:])
                    break

        return text.strip()

    def _call_ai(self, system_prompt: str, user_message: str, max_tokens: int = 2048, temperature: float = 0.3, json_mode: bool = False) -> str:
        """
        OpenRouter API ga so'rov yuborish
        Agar asosiy model ishlamasa, fallback modellarga o'tadi
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/muhammadfayzboss-a11y/FURQON-AI-2",
            "X-Title": "FURQON AI Bot"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        # Har bir modelni sinab ko'rish
        for model in self.all_models:
            payload["model"] = model
            try:
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=90
                )
                data = response.json()

                # Muvaffaqiyatli javob
                if "choices" in data and len(data["choices"]) > 0:
                    content = data["choices"][0]["message"]["content"]
                    if model != self.model:
                        print(f"⚠️ Fallback model ishlatildi: {model}")
                    return content

                # Rate limit xatosi — keyingi modelga o'tish
                error_code = data.get("error", {}).get("code", "")
                if error_code in [429, 404]:
                    print(f"⚠️ {model} — ishlamadi (kod: {error_code}), keyingi model...")
                    continue

                # Boshqa xato
                print(f"⚠️ {model} — xato: {data.get('error', {}).get('message', 'nomaʼlum')}")
                continue

            except requests.exceptions.Timeout:
                print(f"⚠️ {model} — timeout, keyingi model...")
                continue
            except Exception as e:
                print(f"⚠️ {model} — xato: {e}")
                continue

        # Barcha modellar ishlamadi
        print("❌ Barcha AI modellar ishlamadi!")
        return None

    def _extract_topics(self, question: str) -> Dict:
        """
        AI yordamida savoldan mavzularni va ma'noni chiqarish
        """
        system_prompt = """Sen Islom dini bo'yichi ekspertsan. Foydalanuvchi savolini tahlil qil.

MUTLAQ FAQAT JSON qaytar. Hech qanday boshqa matn YOZMA. O'ylash jarayonini YOZMA.

{
  "meaning": "savolning qisqacha ma'nosi",
  "topics": ["mavzu1", "mavzu2"],
  "keywords": ["kalit1", "kalit2"],
  "category": "boshqa"
}

Mavzular: namoz, ro'za, zakot, tavhid, sabr, shukr, tavba, ilim, duo, zikr, jannat, do'zax, axloq, oila, nikoh, ota-ona, sadaqa, infaq, hijob, halol, harom, taqvo, imon, sahobalar, payg'ambar, va hokazo."""

        result_text = self._call_ai(system_prompt, question, max_tokens=300, temperature=0.1, json_mode=True)

        if result_text:
            try:
                # Thinking qismini tozalash
                cleaned = self._clean_response(result_text)
                return json.loads(cleaned)
            except json.JSONDecodeError:
                # JSON topishga urinish
                json_match = re.search(r'\{[^{}]+\}', result_text, re.DOTALL)
                if json_match:
                    try:
                        return json.loads(json_match.group())
                    except json.JSONDecodeError:
                        pass

        # Fallback: AI ishlamasa
        print("⚠️ AI mavzu chiqara olmadi, oddiy qidirish ishlatiladi")
        return {
            "meaning": question,
            "topics": question.lower().split(),
            "keywords": question.lower().split(),
            "category": "boshqa"
        }

    def _generate_answer(self, question: str, meaning: str, quran_results: List[Dict], hadith_results: List[Dict]) -> str:
        """
        AI yordamida to'liq javob yaratish
        """
        # Qur'on oyatlarini matn shakliga keltirish
        quran_texts = ""
        for i, ayat in enumerate(quran_results, 1):
            quran_texts += f"""
{i}. {ayat['surah_name']} surasi, {ayat['ayat']}-oyat
   Arabcha: {ayat['arabic']}
   O'zbekcha: {ayat['uzbek']}
"""

        # Hadislarni matn shakliga keltirish
        hadith_texts = ""
        for i, hadith in enumerate(hadith_results, 1):
            hadith_texts += f"""
{i}. {hadith['collection']} (Raviy: {hadith['narrator']})
   Arabcha: {hadith['arabic']}
   O'zbekcha: {hadith['uzbek']}
"""

        system_prompt = """Sen "FURQON AI" botsan — Qur'on va Hadislar asosida javob berasan.

TAQIQ QILINGAN:
- O'z o'yish jarayoningni yozish MUTLAQ TAQIQ QILINGAN!
- "Let me think", "We need to", "Okay", "Actually" kabi so'zlar bilan boshlash MUMKIN EMAS!
- Faqat TAYYOR, Yakuniy javob berasan!
- Shubha, tahlil, fikr yuritish YOQ!
- Boshqa tilda yozish YOQ! Faqat O'ZBEK tilida!

QOIDALAR:
1. O'zbek tilida, hurmatli va tushunarli javob ber
2. Qur'on va Hadis dalillarini keltir
3. O'zingdan hech narsa qo'shma
4. To'g'ridan-to'g'ri javob ber — "🕌" dan boshla!

Javob formati:

🕌 **[Qisqacha javob]**

📖 **Qur'on dalillari:**
[dalillar]

📚 **Hadis dalillari:**
[dalillar]

💡 **Xulosa:**
[xulosa]"""

        user_prompt = f"""Savol: {question}

Qidiruv natijalari:

QUR'ON OYATLARI:
{quran_texts if quran_texts else "Mos oyat topilmadi"}

HADISLAR:
{hadith_texts if hadith_texts else "Mos hadis topilmadi"}

Endi to'g'ridan-to'g'ri javob ber! O'ylash jarayonini YOZMA!"""

        result = self._call_ai(system_prompt, user_prompt, max_tokens=AI_MAX_TOKENS, temperature=AI_TEMPERATURE)

        if result:
            # Thinking qismini tozalash
            cleaned = self._clean_response(result)
            # Agar tozalangan javob juda qisqa bo'lsa yoki bo'sh bo'lsa, originalni qaytarish
            if len(cleaned) > 50:
                return cleaned
            elif len(result) > 50:
                return result

        # Fallback
        return self._fallback_answer(question, quran_results, hadith_results)

    def _fallback_answer(self, question: str, quran_results: List[Dict], hadith_results: List[Dict]) -> str:
        """AI ishlamaganda oddiy javob formati"""
        answer = f"🕌 **Savol: {question}**\n\n"

        if quran_results:
            answer += "📖 **Qur'on dalillari:**\n\n"
            for i, ayat in enumerate(quran_results, 1):
                answer += f"{i}. *{ayat['surah_name']} surasi, {ayat['ayat']}-oyat*\n"
                answer += f"   🇸🇦 {ayat['arabic']}\n"
                answer += f"   🇺🇿 {ayat['uzbek']}\n\n"

        if hadith_results:
            answer += "📚 **Hadis dalillari:**\n\n"
            for i, hadith in enumerate(hadith_results, 1):
                answer += f"{i}. *{hadith['collection']} — {hadith['narrator']}*\n"
                answer += f"   🇸🇦 {hadith['arabic']}\n"
                answer += f"   🇺🇿 {hadith['uzbek']}\n\n"

        if not quran_results and not hadith_results:
            answer += "⚠️ Kechirasiz, bu savolga mos oyat yoki hadis topilmadi. Boshqacha so'zlar bilan yozib ko'ring.\n\n"

        answer += "🤖 *FURQON AI*"
        return answer

    async def process_question(self, question: str) -> str:
        """
        Asosiy funksiya: savolni qabul qilib, javob qaytarish
        """
        # 1. Savolni tahlil qilish
        analysis = self._extract_topics(question)
        meaning = analysis.get("meaning", question)
        topics = analysis.get("topics", [])
        keywords = analysis.get("keywords", [])

        # 2. Qur'on va Hadislardan qidirish
        quran_results = []
        hadith_results = []

        # Mavzular bo'yicha qidirish
        if topics:
            quran_results.extend(self.search.search_quran("", topics=topics))
            hadith_results.extend(self.search.search_hadith("", topics=topics))

        # Kalit so'zlar bo'yicha qidirish
        for keyword in keywords:
            q_keyword = self.search.search_quran(keyword)
            h_keyword = self.search.search_hadith(keyword)
            quran_results.extend(q_keyword)
            hadith_results.extend(h_keyword)

        # To'g'ridan-to'g'ri savol matni bo'yicha qidirish
        quran_results.extend(self.search.search_quran(question))
        hadith_results.extend(self.search.search_hadith(question))

        # Dublikatlarni olib tashlash (id bo'yicha)
        seen_q = set()
        unique_quran = []
        for item in quran_results:
            if item["id"] not in seen_q:
                seen_q.add(item["id"])
                unique_quran.append(item)

        seen_h = set()
        unique_hadith = []
        for item in hadith_results:
            if item["id"] not in seen_h:
                seen_h.add(item["id"])
                unique_hadith.append(item)

        # Score bo'yicha saralash va chegara
        unique_quran.sort(key=lambda x: x.get("score", 0), reverse=True)
        unique_hadith.sort(key=lambda x: x.get("score", 0), reverse=True)
        unique_quran = unique_quran[:3]
        unique_hadith = unique_hadith[:3]

        # 3. AI bilan javob yaratish
        answer = self._generate_answer(question, meaning, unique_quran, unique_hadith)
        return answer
