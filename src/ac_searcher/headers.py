from random import choice

# Класс для описания хеадров (параметров запроса), можно расширять.
# Позвоялет сохранять некоторые хедеры, например юсер-агент, или тип ожидаемого ответа.
class Headers:
    headers = {}
    
    # Возвращает существущие хедеры. Юсер агент всегда разный.
    def get_headers(self) -> dict:
        self.headers["User-Agent"] = self.getRandomUserAgent()

        return self.headers

    # Добавление нового хедера в запрос. 
    def set_header(self, key, value):
        self.headers[key] = value

    # Удаление хедера
    def remove_header(self, key):
        del self.headers[key]

    @staticmethod
    def getRandomUserAgent() -> str:
        user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
                       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
                       #"Opera/9.80 (Windows NT 6.2; Win64; x64) Presto/2.12.388 Version/12.17"
                       ]
        
        # showed some erros because of request to mobile
        #
                    # "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1)",
                    # "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
                    # "Opera/9.80 (Windows NT 6.2; Win64; x64) Presto/2.12.388 Version/12.17"]
        return choice(user_agents)