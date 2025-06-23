from utils.llm import ask_llm
from utils.logger import get_logger

logger = get_logger("search")

class SearchAgent:
    def run(self, params: dict):
        question = params.get("question", "")
        logger.debug(f"SearchAgent reçoit la question : {question}")

        prompt = f"Réponds à la question suivante :\n\nQuestion : {question}"
        answer = ask_llm(prompt)

        logger.info("SearchAgent a terminé")
        return answer
