import requests
from bs4 import BeautifulSoup
from utils.llm import ask_llm
from utils.logger import get_logger

logger = get_logger("scraper")

class ScraperAgent:
    def run(self, params: dict):
        url = params.get("url")
        question = params.get("question", "Fais un résumé du contenu")

        logger.debug(f"Scraping URL: {url} with question: {question}")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # lève une exception si le status != 200

            soup = BeautifulSoup(response.text, "html.parser")

            # Extraire le texte visible (sans scripts, styles, etc.)
            page_text = soup.get_text(separator="\n", strip=True)

            # Réduction du texte si trop long (LLM limité à ~4k tokens)
            max_length = 4000
            page_text = page_text[:max_length]

            prompt = f"{question}\n\nContenu de la page :\n{page_text}"
            answer = ask_llm(prompt)

            logger.info("Scraper a terminé")
            return answer

        except requests.RequestException as e:
            logger.error(f"Erreur lors de l'accès à l'URL : {e}")
            return "❌ Impossible d'accéder à la page. Vérifie que le lien est valide et accessible."