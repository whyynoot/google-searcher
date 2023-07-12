# Link класс для описания ссылки, найденной в результате поиска в Searchers
class Link: 
    # url - ссылка
    url = ""
    # name - краткое описание сформированное поисковиком
    name = ""
    # source - из какого поисковика, или системы пришла данная ссылка
    source = ""
    # какой постфикс присутсвовал в поисковом запросе (чаще всего это будет регион)
    postfix = ""

    # Конструктор нашей ссылки
    def __init__(self, url, name, source):
        self.url = url
        self.name = name
        self.source = source
        print(f'Initialized link', self)
    
    # Сеттер для постфикса. Позволяет задать значени постфикса
    def set_postfix(self, postfix):
        self.postfix = postfix
    
    # репрезентация нашей ссылки в строке
    def __str__(self) -> str:
        return f'URL: {self.url} | Name: {self.name} | Source: {self.source}'