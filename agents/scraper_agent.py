from utils.llm import ask_llm
from utils.logger import get_logger
logger = get_logger("scraper")

class ScraperAgent:
    def run(self, params: dict):
        url = params.get("url")
        question = params.get("question", "Fais un résumé du contenu")

        logger.debug(f"Scraping URL: {url} with question: {question}")
        
        # 👉 Simuler récupération du texte (à remplacer plus tard)
        simulated_text = f"Voici le contenu HTML simulé extrait de {url}..."
        
        prompt = f"{question}\n\nContenu de la page :\n{simulated_text}"
        answer = ask_llm(prompt)
        
        logger.info("Scraper a terminé")
        return answer
