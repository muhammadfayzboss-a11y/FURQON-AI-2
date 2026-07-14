"""
FURQON AI - AI Handler
OpenRouter orqali AI bilan ishlash (Gemini 2.0 Flash — BEPUL!)
"""

import json
from typing import Dict, List
from openai import OpenAI
from config import OPENROUTER_API_KEY, AI_BASE_URL, AI_MODEL, AI_MAX_TOKENS, AI_TEMPERATURE
from search_engine import SearchEngine


class AIHandler:
    """AI yordamida savollarga javob berish"""

    def __init__(self):
        self.client = OpenAI(
            base_url=AI_BASE_URL,
            api_key=OPENROUTER_API_KEY,
        )
        self.search = SearchEngine()

    def _extract_topics(self, question: str) -> Dict:
        """
        AI yordamida savoldan mavzularni va ma'noni chiqarish
        """
        system_prompt = """Sen Islom dini bo'yicha ekspertsan. Foydalanuvchining savolini tahlil qilib:
1. Savolning asosiy ma'nosini tushun
2. Qaysi Islomiy mavzularga aloqadorligini aniqla
3. Qidiruv uchun kalit so'zlar va mavzularni chiqar

Javobni FAQAT quyidagi JSON formatda bering, hech qanday qo'shimcha matn yozma:
{
  "meaning": "savolning qisqacha ma'nosi o'zbek tilida",
  "topics": ["mavzu1", "mavzu2", "mavzu3"],
  "keywords": ["kalit1", "kalit2", "kalit3"],
  "category": "namoz|ro'za|zakot|haj|tavhid|axloq|duo|sabr|shukr|ilim|jannat|do'zax|tavba|nikoh|oila|huquq|boshqa"
}

Mavzular o'zbek tilida bo'lsin. Masalan: namoz, ro'za, zakot, tavhid, shirk, sabr, shukr, tavba, 
ilim, duo, zikr, jannat, do'zax, axloq, oila, nikoh, ota-ona, qo'shni, sadaqa, infaq, 
hijob, halol, harom, taqvo, imon, kufr, nifoq, hijrat, jihod, payg'ambar, sahobalar, va hokazo."""

        try:
            response = self.client.chat.completions.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                max_tokens=500,
                temperature=0.1,
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            print(f"⚠️ AI mavzu chiqarishda xato: {e}")
            return {
                "meaning": question,
                "topics": [question.lower()],
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
   Arabча: {ayat['arabic']}
   O'zbekcha: {ayat['uzbek']}
"""

        # Hadislarni matn shakliga keltirish
        hadith_texts = ""
        for i, hadith in enumerate(hadith_results, 1):
            hadith_texts += f"""
{i}. {hadith['collection']} (Raviy: {hadith['narrator']})
   Arabча: {hadith['arabic']}
   O'zbekcha: {hadith['uzbek']}
"""

        system_prompt = f"""Sen "FURQON AI" — Qur'on va Hadislar asosida javob beruvchi Islomiy bilim botsan.

QOIDALAR:
1. Javobni o'zbek tilida, tushunarli va hurmatli tarzda ber
2. Har bir dalilni Qur'on yoki Hadis bilan mustahkamla
3. Oyat va hadislarni to'g'ri keltir
4. O'zingdan hech narsa qo'shma, faqat keltirilgan manbalarga tayangan holda tushuntir
5. Agar savolga aniq javob topolmasang, shuni ayt
6. Javobni chiroyli formatda, emoji bilan bezaklab ber

Foydalanuvchi savoli: {question}
Savolning ma'nosi: {meaning}

TOPILGAN QUR'OON OYATLARI:
{quran_texts if quran_texts else "Aynan mos oyat topilmadi"}

TOPILGAN HADISLAR:
{hadith_texts if hadith_texts else "Aynan mos hadis topilmadi"}

Endi quyidagi strukturada javob ber:

🕌 **[Savolning qisqacha javobi]**

📖 **Qur'on dalillari:**
[Har bir oyatni keltirib, tushuntirish]

📚 **Hadis dalillari:**
[Har bir hadisni keltirib, tushuntirish]

💡 **Xulosa:**
[Qisqacha xulosa va maslahat]"""

        try:
            response = self.client.chat.completions.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                max_tokens=AI_MAX_TOKENS,
                temperature=AI_TEMPERATURE,
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"⚠️ AI javob yaratishda xato: {e}")
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
