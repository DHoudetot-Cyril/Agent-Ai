from utils.llm import ask_llm
from utils.logger import get_logger

logger = get_logger("JokeAgent")

class JokeAgent:
    def run(self, params: dict):
        category = params.get("question", "").strip().lower()
        logger.debug(f"JokeAgent reçoit la requête : {category}")

        if category:
            prompt = f"Raconte une blague courte, drôle et originale sur le thème suivant : {category}. Réponds uniquement avec la blague, en français."
        else:
            prompt = "Raconte une blague courte, drôle et originale. Réponds uniquement avec la blague, en français."

        try:
            answer = ask_llm(prompt)
        except Exception as e:
            logger.error(f"Erreur JokeAgent : {e}")
            return "❌ Je n'ai pas réussi à faire une blague cette fois..."

        logger.info("JokeAgent a terminé")
        return answer