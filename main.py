import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# 1. Загружаем ключи из файла .env
load_dotenv()
my_token = os.getenv("GITHUB_TOKEN")

# ПРОВЕРКА: Видит ли код ключ?
if not my_token:
    print("ОШИБКА: Код не видит токен! Проверь файл .env")
else:
    print("ТОКЕН НАЙДЕН. Подключаюсь к Llama...")

# 2. Настройка подключения к GitHub Models
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=my_token
)

def get_advice():
    try:
        # Читаем твоих игроков
        with open('squad.json', 'r', encoding='utf-8') as f:
            players = json.load(f)
        
        prompt = f"Вот мои молодые игроки: {players}. Кто из них самый перспективный и какую тренировку ему назначить?"

        # ЗАПРОС К НЕЙРОНКЕ
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="meta-llama-3.1-8b-instruct"
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка при запросе: {e}"

if __name__ == "__main__":
    if my_token:
        print("--- ИИ-Тренер анализирует состав... ---")
        print(get_advice())
