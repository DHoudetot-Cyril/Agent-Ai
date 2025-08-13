# Agent-Ai

 Un orchestrateur multi-agents simple pour router les requêtes utilisateur vers plusieurs capacités :

 - Scraping d'URL et résumé via LLM (`scraper`)
 - RAG sur documents PDF locaux (`rag`)
 - Réponse générale via LLM (`search`)
 - Génération de blagues (`joke`)

## Architecture

- `main.py` : interface CLI. Transforme une question utilisateur en une requête JSON (via LLM) et l'envoie à l'orchestrateur.
- `orchestrator.py` : routeur qui délègue aux agents selon `function` ∈ {`scraper`, `rag`, `search`, `joke`}.
- `agents/` :
  - `scraper_agent.py` : récupère la page avec `requests`, parse avec `BeautifulSoup`, résume via LLM.
  - `rag_agent.py` : initialise un moteur RAG et répond à partir des PDF de `source/`.
  - `rag_engine.py` : extraction PDF, embeddings (SentenceTransformers), recherche par similarité, composition du prompt, appel LLM.
  - `search_agent.py` : recherche avec DuckDuckGo (`duckduckgo-search`), synthèse via LLM.
  - `joke_agent.py` : génère une blague courte en français via LLM.
- `utils/`
  - `llm.py` : client OpenAI-compatible (API clé/base_url, modèle), appel en streaming.
  - `logger.py` : configuration logger.
- `source/` : répertoire attendu pour vos PDF (non versionnés ici).

## Prérequis

- Python 3.10+
- Accès à une API OpenAI-compatible (hébergée localement ou distante). Le projet est utilisé avec llama.cpp en local (serveur OpenAI-compatible). Par défaut : `base_url="http://localhost:8080/v1"` et un modèle configuré côté serveur dans `utils/llm.py`.
- GPU facultatif mais recommandé pour `sentence-transformers` (installe `torch` compatible avec ton CUDA si nécessaire).

## Installation

1) Créer et activer un environnement virtuel

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Installer les dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3) Configurer l'accès LLM

Éditer `utils/llm.py` :

- Remplacer `api_key` par votre clé réelle (`OPENAI_API_KEY`), ou charger depuis l'environnement.
- Ajuster `base_url` si vous utilisez Ollama/LM Studio ou une instance OpenAI-compatible.
- Mettre `LLM_MODEL_NAME` au nom du modèle disponible côté serveur.

Exemple (environnement) :

```python
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))
LLM_MODEL_NAME = os.getenv("OPENAI_MODEL", "qwen2.5:7b")
```

4) Ajouter vos documents PDF

Placez vos fichiers `.pdf` dans le dossier `source/`. Le moteur RAG les indexe au lancement de `RagAgent`.

## Utilisation (CLI)

Lancer le routeur :

```bash
python main.py
```

Saisissez une question. Le `main.py` demande au LLM de produire un JSON d'appel d'agent. Règles de routage :

- **scraper** : pour une URL + question
  - Exemple : « Résume cette page https://fr.wikipedia.org/wiki/Jeanne_d%27Arc »
- **rag** : pour une question à répondre exclusivement à partir des PDF locaux
  - Exemple : « Selon les documents internes, quelles sont les conclusions clés sur … »
- **search** : question générale sans URL ni contrainte documents internes
 - **joke** : si le mot « blague » apparaît, l'agent de blague est appelé. Le paramètre `question` devient la catégorie
   - Exemple : « Fais-moi une blague sur les développeurs »

Le JSON produit est ensuite envoyé à l'orchestrateur qui appelle l'agent correspondant.

## Personnalisation

- `agents/scraper_agent.py` : ajuster le scraping (ex. gestion d'encodage, user-agent, anti-bot, ou `playwright`).
- `agents/rag_engine.py` :
  - Modifier `EMBEDDING_MODEL` (par défaut : `intfloat/multilingual-e5-large-instruct`).
  - Ajuster `k` pour le nombre de passages récupérés.
  - Ajouter un prétraitement (chunking, nettoyage) si vos PDF sont volumineux.
- `utils/llm.py` : activer la lecture des variables d'environnement et gérer les erreurs réseau.

### Utilisation avec llama.cpp (local)

L'application est conçue pour fonctionner avec un serveur OpenAI-compatible fourni par llama.cpp.

Exemple de lancement du serveur (adapter le chemin du modèle) :

```bash
./server -m /chemin/vers/modele.gguf -c 4096 -ngl 20 -t 8 --host 127.0.0.1 --port 8080 --api
```

Remarques :
- L'option `--api` active l'API OpenAI-compatible sur `http://localhost:8080/v1`.
- Assurez-vous que `base_url` dans `utils/llm.py` (ou la variable `OPENAI_BASE_URL`) pointe vers cette URL et se termine bien par `/v1`.

## Variables d'environnement suggérées

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_BASE_URL="http://localhost:8080/v1"
export OPENAI_MODEL="qwen2.5:7b"
```

Adapter ces variables à votre fournisseur de LLM.

## Dépannage

- Aucun PDF détecté : vérifiez que le dossier `source/` contient des `.pdf` lisibles.
- Erreur torch/cuda : installez une version de `torch` compatible avec votre CUDA, ou utilisez CPU.
- 401/404 côté LLM : vérifiez `api_key`, `base_url` et `LLM_MODEL_NAME`.
- JSON invalide généré par le LLM dans `main.py` : reformulez la question pour respecter les règles, ou durcissez le parsing.

## Licence

Projet éducatif/expérimental. À adapter selon vos besoins.


