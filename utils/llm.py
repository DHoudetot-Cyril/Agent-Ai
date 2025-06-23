from openai import OpenAI

# Adapter avec ton vrai endpoint et modèle
client = OpenAI(
    api_key="1234",
    base_url="http://localhost:8080"  # Ollama ou autre serveur local
)

LLM_MODEL_NAME = "qwen_truc"

def ask_llm(prompt: str, system: str = "Tu es un assistant utile qui répond uniquement en français.") -> str:
    
    #print(f"\n\n\n\n\n[ASKLLM] Appel LLM de base avec prompt : {prompt} et system : {system}\n\n\n\n\n")
    messages = [
        {"role": "system", "content": system + " </no_think> " },
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model=LLM_MODEL_NAME,
        messages=messages,
        temperature=0.7,
        max_tokens=1000,
        stream=True  # Utiliser le streaming pour des réponses plus rapides
    )
    

    answer = ""
    print("🧠 Réponse :", end=" ", flush=True)
    for chunk in response:
        delta = chunk.choices[0].delta
        content = delta.content or ""
        print(content, end="", flush=True)
        answer += content
    print("\n")  # saut de ligne
    return answer