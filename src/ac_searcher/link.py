# Link класс для описания ссылки, найденной в результате поиска в Searchers
class Link: 
    postfix = ""

    # Конструктор нашей ссылки
    def __init__(self, url: str, name: str, source: str):
        # url - ссылка
        self.url = url
        # name - краткое описание сформированное поисковиком
        self.name = name
        # source - из какого поисковика, или системы пришла данная ссылка
        self.source = source
        #print(f'Initialized link', self)
    
    # Сеттер для постфикса. Позволяет задать значени постфикса
    def set_postfix(self, postfix: str):
        self.postfix = postfix
    
    # репрезентация нашей ссылки в строке
    def __str__(self) -> str:
        return f'URL: {self.url} | Name: {self.name} | Source: {self.source}'