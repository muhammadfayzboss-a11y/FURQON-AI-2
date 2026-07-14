"""
FURQON AI - Qidiruv tizimi
Qur'on oyatlari va Hadislarni qidirish va filtrlash
"""

import json
from typing import List, Dict, Optional
from config import QURAN_DATA_PATH, HADITH_DATA_PATH, MAX_QURAN_AYATS, MAX_HADITHS


class SearchEngine:
    """Qur'on va Hadis ma'lumotlar bazasidan qidirish"""

    def __init__(self):
        self.quran_data = self._load_data(QURAN_DATA_PATH)
        self.hadith_data = self._load_data(HADITH_DATA_PATH)

    def _load_data(self, path: str) -> List[Dict]:
        """JSON fayldan ma'lumotlarni yuklash"""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Ma'lumotlar fayli topilmadi: {path}")
            return []
        except json.JSONDecodeError:
            print(f"⚠️ JSON formati xato: {path}")
            return []

    def search_quran(self, query: str, topics: List[str] = None) -> List[Dict]:
        """
        Qur'on oyatlarini qidirish
        - query: qidiruv so'zi
        - topics: mavzu ro'yxati (ixtiyoriy)
        """
        results = []
        query_lower = query.lower()

        for ayat in self.quran_data:
            score = 0

            # Matn bo'yicha qidirish
            if query_lower in ayat.get("uzbek", "").lower():
                score += 10

            # Mavzular bo'yicha qidirish
            if topics:
                for topic in topics:
                    if topic.lower() in [t.lower() for t in ayat.get("topics", [])]:
                        score += 5
            else:
                # So'zni mavzularda qidirish
                for topic in ayat.get("topics", []):
                    if query_lower in topic.lower() or topic.lower() in query_lower:
                        score += 3

            # Sura nomi bo'yicha
            if query_lower in ayat.get("surah_name", "").lower():
                score += 7

            if score > 0:
                results.append({**ayat, "score": score})

        # Score bo'yicha saralash
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:MAX_QURAN_AYATS]

    def search_hadith(self, query: str, topics: List[str] = None) -> List[Dict]:
        """
        Hadislarni qidirish
        - query: qidiruv so'zi
        - topics: mavzu ro'yxati (ixtiyoriy)
        """
        results = []
        query_lower = query.lower()

        for hadith in self.hadith_data:
            score = 0

            # Matn bo'yicha qidirish
            if query_lower in hadith.get("uzbek", "").lower():
                score += 10

            # Mavzular bo'yicha qidirish
            if topics:
                for topic in topics:
                    if topic.lower() in [t.lower() for t in hadith.get("topics", [])]:
                        score += 5
            else:
                for topic in hadith.get("topics", []):
                    if query_lower in topic.lower() or topic.lower() in query_lower:
                        score += 3

            # To'plam nomi bo'yicha
            if query_lower in hadith.get("collection", "").lower():
                score += 7

            # Raviy nomi bo'yicha
            if query_lower in hadith.get("narrator", "").lower():
                score += 5

            if score > 0:
                results.append({**hadith, "score": score})

        # Score bo'yicha saralash
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:MAX_HADITHS]

    def get_all_topics(self) -> Dict[str, List[str]]:
        """Barcha mavzularni olish"""
        quran_topics = set()
        hadith_topics = set()

        for ayat in self.quran_data:
            for topic in ayat.get("topics", []):
                quran_topics.add(topic)

        for hadith in self.hadith_data:
            for topic in hadith.get("topics", []):
                hadith_topics.add(topic)

        return {
            "quran_topics": sorted(list(quran_topics)),
            "hadith_topics": sorted(list(hadith_topics))
        }

    def search_by_surah(self, surah_number: int) -> List[Dict]:
        """Sura raqami bo'yicha qidirish"""
        return [
            ayat for ayat in self.quran_data
            if ayat.get("surah") == surah_number
        ]

    def get_random_ayat(self) -> Optional[Dict]:
        """Tasodifiy oyat olish"""
        import random
        if self.quran_data:
            return random.choice(self.quran_data)
        return None

    def get_random_hadith(self) -> Optional[Dict]:
        """Tasodifiy hadis olish"""
        import random
        if self.hadith_data:
            return random.choice(self.hadith_data)
        return None
