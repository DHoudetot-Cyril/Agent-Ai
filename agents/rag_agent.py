from utils.logger import get_logger
from agents.rag_engine import initialize_rag, rag_answer

logger = get_logger("rag")

class RagAgent:
    def __init__(self):
        logger.info("Initialisation du moteur RAG...")
        self.docs, self.embedder, self.doc_embeddings = initialize_rag()
        logger.info("Documents et embeddings chargés.")

    def run(self, params: dict):
        question = params.get("question")
        logger.debug(f"Question posée au RAG : {question}")

        answer = rag_answer(question, self.embedder, self.docs, self.doc_embeddings)

        logger.info("RAG a terminé")
        return answer
