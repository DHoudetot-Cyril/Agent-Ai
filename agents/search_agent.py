from utils.llm import ask_llm
from utils.logger import get_logger
from duckduckgo_search import DDGS

logger = get_logger("search")

class SearchAgent:
    def run(self, params: dict):
        question = params.get("question", "")
        logger.debug(f"SearchAgent reçoit la question : {question}")

        try:
            with DDGS() as ddgs:
                results = ddgs.text(question, max_results=3)
                context = "\n".join(
                    f"{r.get('title', '')} : {r.get('body', '')}\nLien : {r.get('href', '')}"
                    for r in results
                )

            logger.debug("Résultats DuckDuckGo combinés pour le LLM.")
            prompt = (
                f"Voici les informations trouvées sur Internet :\n{context}\n\n"
                f"En te basant uniquement sur ces résultats, réponds à la question :\n{question}"
            )

            answer = ask_llm(prompt)

        except Exception as e:
            logger.error(f"Erreur de recherche DuckDuckGo : {e}")
            answer = "❌ Une erreur est survenue lors de la recherche sur Internet."

        logger.info("SearchAgent a terminé")
        return answer