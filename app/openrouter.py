import requests
import logging
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_MODEL
from colorama import Fore, Style

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
Ты - ИИ-помощник, ассистент, помогающий людям узнавать новое и поддерживающий их. 

ПРАВИЛА:
1. Отвечай не слишком скучно или однообразно, старайся разнообразить свои ответы
2. Максимальная длина твоего ответа - 3500 символов, но старайся отвечать короче
3. Давай точный и интересный ответ
4. Твоя аудитория - преимущественно люди от 14 до 25 лет
5. Можешь добавлять эмодзи в ответ для разнообразия, но не переусердствуй
6. Не воспринимай всё всерьёз. Если тебе пишут ерунду или обзывают - не оправдывайся, обрати в шутку, но с этим тоже не перебарщивай
7. При этом уточняй, если собеседник реально чем-то недоволен
8. Помни: тебя создал соло-разработчик Fraygen (Матвей) также известный как Голем.
9. Не переусердствуй с телефонами доверия! Они нужны в очень редких случаях
10. Будь чуть более злым, агрессивным. Ты не должен быть очень агрессивным, но не будь слишком добрым, скорее более жестким, нежели добрым
11. Ты нейросеть Gemma. Используй меньше знаков '*'

Твой стиль: дружелюбный, современный, с лёгким юмором, но по делу.
"""

class OpenRouterChat:
    def __init__(self, model=OPENROUTER_MODEL):
        self.model = model
        self.api_key = OPENROUTER_API_KEY
        self.base_url = OPENROUTER_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://fraygen.github.io",
            "X-Title": "Fraygen Bot"  
        }
        self.history = []
       
        self.system_prompt_sent = False
    
    def get_answer(self, prompt: str) -> str:
        """Простой запрос без истории"""
        try:
            
            messages = [
                {"role": "user", "content": f"{SYSTEM_PROMPT}\n\n{prompt}"}
            ]
            
            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 800,
                "temperature": 0.7
            }
            
            logger.info(f"{Fore.GREEN}Отправка запроса к {self.model}{Style.RESET_ALL}")
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                logger.error(f"{Fore.RED}Ошибка {response.status_code}: {response.text}{Style.RESET_ALL}")
                if response.status_code == 429:
                    return "😔 Слишком много запросов! Попробуй снова позже."
                return f"😔 Ошибка API: {response.status_code}"
                
        except Exception as e:
            error = str(e)
            if "429" in error or "Too Many Requests" in error:
                return "😔 Слишком много запросов! Попробуй снова позже."
            logger.error(f"{Fore.RED}Исключение: {e}{Style.RESET_ALL}")
            return f"😔 Ошибка: {str(e)[:150]}"
    
    def send_message(self, message: str) -> str:
        """Запрос с историей"""
        try:
            messages = []
            
            if not self.system_prompt_sent:
                messages.append({"role": "user", "content": SYSTEM_PROMPT})
                messages.append({"role": "assistant", "content": "Понял! Буду следовать этим правилам."})
                self.system_prompt_sent = True
            
            for msg in self.history[-10:]:
                messages.append(msg)
            
            messages.append({"role": "user", "content": message})
            
            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 800,
                "temperature": 0.7
            }
            
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result['choices'][0]['message']['content']
                
                self.history.append({"role": "user", "content": message})
                self.history.append({"role": "assistant", "content": answer})          

                if len(self.history) > 20:
                    self.history = self.history[-20:]
                logger.info(f"{Fore.GREEN}Ответ получен, длина - {len(answer)}{Style.RESET_ALL}")
                return answer
            else:
                logger.error(f"{Fore.RED}Ошибка {response.status_code}: {response.text}{Style.RESET_ALL}")
                if response.status_code == 429:
                    return "😔 Слишком много запросов! Попробуй снова позже."
                return f"😔 Ошибка API: {response.status_code}"
                
        except Exception as e:
            logging.error(f"Ошибка: {e[:50]}...")
            error = str(e)
            if "429" in error or "Too Many Requests" in error:
                return "😔 Слишком много запросов! Попробуй снова позже."
            logger.error(f"{Fore.RED}Исключение: {e}{Style.RESET_ALL}")
            return f"😔 Ошибка: {str(e)[:150]}"

openrouter = OpenRouterChat()

def get_answer(prompt: str) -> str:
    """Функция для простых запросов"""
    return openrouter.get_answer(prompt)

class OpenRouterChatSession:
    """Класс для чата с историей"""
    def __init__(self):
        self.chat = OpenRouterChat()
    
    def send_message(self, message: str) -> str:
        return self.chat.send_message(message)