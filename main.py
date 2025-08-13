from orchestrator import handle_request
from utils.llm import ask_llm
import json
import re

def help():
    print(
       "Pose ta question à l'orchestrateur (ex: Résume cette page https://fr.wikipedia.org/wiki/Jeanne_d%27Arc)\n\n"
        "Règles :\n"
        '- Si la question concerne une URL, utilise "function": "scraper" et donne "url" + une "question".\n'
        '- Si la question concerne un sujet qui doit être répondu uniquement à partir des documents internes, utilise "function": "rag" et fournis "question".\n'
        '- Si c\'est une question générale sans URL et sans mention de documents internes, utilise "function": "search" avec la "question" comme paramètre.\n'
    )

def main():
    print("Bienvenue dans l'orchestrateur intelligent !")
    print("Pose ta question et je te guiderai vers la bonne réponse.\n")
    help()

    system_prompt = """Tu es un routeur intelligent. Tu dois répondre uniquement en JSON.
    
Ta tâche est de convertir la question de l'utilisateur en un appel d'agent structuré sous la forme :
{
  "function": "scraper" | "rag" | "search" | "joke",
  "params": {
    ... paramètres nécessaires ...
  }
}

Règles :
- Si la question concerne une URL, utilise "function": "scraper" et donne "url" + une "question".
- Si la question concerne un sujet qui doit être répondu uniquement à partir des documents internes, utilise "function": "rag" et fournis "question".
- Si c'est une question générale sans URL et sans mention de documents internes, utilise "function": "search" avec la "question" comme paramètre.
- Si le mot blague est mentionné, réponds avec "function": "joke" et un paramètre "question" qui sert de catégorie à la blague.
- Ne retourne jamais autre chose que le JSON valide."""

    while True:
        user_query = input("\n\n\nPose ta question (ou 'exit' pour quitter) >> ")
        if user_query.lower() in {"exit", "quit"}:
            print("👋 Au revoir !")
            break
        if user_query.lower() in {"help"}:
            help()
            continue

        try:
            json_response = ask_llm(user_query, system=system_prompt)
            #print(f"\n🔁 JSON généré par le LLM :\n{json_response}")

            # Cherche un bloc JSON valide dans toute la réponse
            match = re.search(r'\{[\s\S]*\}', json_response)
            if not match:
                raise ValueError("Aucun bloc JSON trouvé.")

            json_str = match.group(0)
            #print("📦 JSON extrait :", json_str)

            parsed_request = json.loads(json_str)
            result = handle_request(parsed_request)

            #print("\n✅ Résultat final :")
            #print(result)

        except json.JSONDecodeError as e:
            print("❌ Erreur : le LLM n'a pas généré un JSON valide.")
            print(json_response)
        except Exception as e:
            print(f"❌ Erreur d'exécution : {e}")

if __name__ == "__main__":
    main()