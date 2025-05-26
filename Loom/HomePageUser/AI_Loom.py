import requests
import json
from Key_API import KeyAPI

# Ввод задач с консоли
print("Введите задачи через запятую (например: купить продукты, сделать отчет, позвонить врачу):")
tasks_input = input()
tasks = [task.strip() for task in tasks_input.split(",") if task.strip()]

# Формируем промпт
prompt = (
    "Распредели задачи которые я тебе дал, на день по важности и времени выбери лучшее время для каждой задачи."
    "Вот список задач:\n" +
    "\n".join(f"- {task}" for task in tasks)
)

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {KeyAPI}",
        "Content-Type": "application/json",
    },
    data=json.dumps({
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
    })
)

# Выводим только текст ответа
print(response.json()["choices"][0]["message"]["content"])