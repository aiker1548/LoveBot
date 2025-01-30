import requests

class SaigaAPI:
    def __init__(self, base_url: str, model_name: str):
        self.base_url = base_url
        self.model_name = model_name
    
    def generate_response(self, prompt: str) -> str:
        """
        Отправляет запрос к нейронке и возвращает сгенерированный ответ.

        :param prompt: Промт, который будет отправлен нейронке
        :return: Ответ от нейронки
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Проверяем наличие ошибок HTTP
            result = response.json()
            print(result)
            return result.get("response", "Ошибка: пустой ответ от нейронки")
        
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к нейронке: {e}")
            return "Ошибка при запросе к нейронке"

import json
import requests

stream = False
url = "https://proxy.tune.app/chat/completions"
headers = {
    "Authorization": "sk-tune-BELpvAnsGjIkivwA6j9ufwynF7Gx9EhpInp",
    "Content-Type": "application/json",
}
data = {
    "temperature": 0.8,
    "messages": ['че скажешь бро?'],
    "model": "deepseek/deepseek-r1",
    "stream": stream,
    "frequency_penalty": 0,
    "max_tokens": 900
}

try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Проверяем наличие ошибок HTTP
    
    if response.text:  # Проверяем, что ответ не пустой
        if stream:
            for line in response.iter_lines():
                if line:
                    l = line[6:]
                    if l != b'[DONE]':
                        print(json.loads(l))
        else:
            print(response.json())
    else:
        print("Пустой ответ от сервера")
except requests.exceptions.RequestException as e:
    print(f"Ошибка при запросе к серверу: {e}")

# # Пример использования
# if __name__ == "__main__":
#     base_url = "http://localhost:11434"
#     model_name = "bambucha/saiga-llama3"
    
#     saiga_api = SaigaAPI(base_url, model_name)
    
#     # Пример промта
#     message_from_masha = "Сегодня немного устала, но стараюсь успеть все дела к вечеру."
#     prompt = f"Маша пишет: \"{message_from_masha}\"\nОтветь ей комплиментом, который подбодрит и подчеркнет ее усилия."
    
#     response = saiga_api.generate_response(prompt)
#     print("Ответ от нейронки:", response)
