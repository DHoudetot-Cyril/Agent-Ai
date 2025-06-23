from agents.scraper_agent import ScraperAgent
from agents.rag_agent import RagAgent
from agents.search_agent import SearchAgent
from utils.logger import get_logger

logger = get_logger("orchestrator")

AGENTS = {
    "scraper": ScraperAgent(),
    "rag": RagAgent(),
    "search": SearchAgent(),
}

def handle_request(request: dict):
    logger.debug(f"Requête reçue : {request}")
    function = request.get("function")
    params = request.get("params", {})

    agent = AGENTS.get(function)
    if not agent:
        logger.error(f"Agent inconnu : {function}")
        return {"error": f"Fonction inconnue : {function}"}

    try:
        result = agent.run(params)
        logger.debug(f"Résultat de {function} : {result}")
        return {"function": function, "response": result}
    except Exception as e:
        logger.exception("Erreur pendant l'exécution de l'agent")
        return {"error": str(e)}
