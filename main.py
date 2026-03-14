import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Инициализация клиента GitHub Models
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ.get("GITHUB_TOKEN") # Убедись, что токен в .env
)

def load_squad():
    with open('squad.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def get_training_advice():
    squad = load_squad()
    
    # Формируем промпт, заставляя ИИ анализировать данные
    prompt = f"""
    Ты — ИИ-ассистент футбольного тренера. Твоя задача — развивать молодежь.
    Вот текущий список игроков: {json.dumps(squad, ensure_ascii=False)}
    
    Исходя из их потенциала и игрового времени в прошлом матче:
    1. Кому из них НУЖНО дать больше времени в следующей игре?
    2. Составь краткий план тренировок на неделю для каждого.
    Отвечай четко, по-спортивному.
    """

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="meta-llama-3.1-8b-instruct",
        temperature=0.7
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    print("--- Анализ состава запущен ---")
    advice = get_training_advice()
    print(advice)

