import xml.etree.ElementTree as ET
tree = ET.parse('verbetesWikipedia.xml')

class Page:
    def __init__(self, id: str, title: str, text: str) -> None:
        self.__id = id
        self.__title = title
        self.__text = text
        
    def getID(self) -> str:
        return self.__id
    
    def getTitle(self) -> str:
        return self.__title
    
    def getText(self) -> str:
        return self.__text

class Search:
    def __init__(self):
        # Tag raiz do XML
        self.root = tree.getroot()
        # Dicionario para armazenar indice invertido
        self.hash = {}

    def createHash(self) -> None:
        # Iterar sobre cada elemento <page>
        for child in self.root:
            # Recupera as informações id, título e texto do XML
            id = child[0].text
            title = child[1].text
            text = child[2].text
            
            # Passa todos os caracteres do título para maiúsculo
            title = title.lower()
            
            # Instancia um objeto Page e atribui o id, titulo e texto da página
            page = Page(id, title, text)
            
            # Cria uma lista de palavras contidas no título
            words = title.split(' ')
            
            # Itera sobre cada palavra do título
            for word in words:
                if word in self.hash:
                    # Adiciona o objeto da página em uma lista que está associada a uma posição do hash
                    self.hash[word].append(page)
                else:
                    # Cria uma lista associada a posição do hash e adiciona o primeiro objeto
                    self.hash[word] = []
                    self.hash[word].append(page)
                    
    def createHash_2(self) -> None:
        # Iterar sobre cada elemento <page>
        for child in self.root:
            # Recupera as informações id, título e texto do XML
            id = child[0].text
            title = child[1].text
            text = child[2].text
            
            # Passa todos os caracteres do título e do texto para maiúsculo
            title = title.lower()
            text = text.lower()
            
            # Instancia um objeto Page e atribui o id, titulo e texto da página
            page = Page(id, title, text)
            
            # Junta o título com o texto para montar o hash com base em uma string só
            words = title + ' ' + text
            
            # Cria uma lista de palavras contidas no título e no texto
            words = words.split(' ')
            
            # Itera sobre cada palavra do título
            for word in words:
                if word in self.hash:
                    # Adiciona o objeto da página em uma lista que está associada a uma posição do hash
                    self.hash[word].append(page)
                else:
                    # Cria uma lista associada a posição do hash e adiciona o primeiro objeto
                    self.hash[word] = []
                    self.hash[word].append(page)

    def searchByTitle(self, word: str) -> None:
        word = self.handleInput(word) 
        # word = word.lower()
        # Tratamento de erro para chaves não encontradas no dicionário
        try:
            # Lista dos itens encontrados para a chave pesquisada
            pages = self.hash[word]
            
            print(f"Títulos que possuem a palavra {word}:")
            for page in pages:
                print(f"{page.getID()} - {page.getTitle()}")
                
            print(f"Total de títulos encontrados: {len(pages)}")
        except KeyError:
            print(f"[Palavra '{word}' não encontrada no hash]")
            
    def searchForRelevance(self, word: str) -> None:
        word = self.handleInput(word)
        occurrencesList = {}
        
        try:
            # Lista dos itens encontrados para a chave pesquisada
            pages = self.hash[word]
            sortedList = []
            
            # Guardando objeto como chave e quantidade de ocorrências como valor em itens de um dicionário
            for page in pages:
                id = page.getID()
                title = page.getTitle()
                text = page.getText()
                
                occurrencesInTitle = title.count(word)
                occurrencesInText = text.count(word)
                
                if occurrencesInTitle > 0:
                    occurrences = occurrencesInText * 2
                else:
                    occurrences = occurrencesInText
                    
                
                occurrencesList[page] = occurrences

            # Criando uma lista com os objetos ordenados por quantidade de ocorrências em ordem decrescente
            for page in sorted(occurrencesList, key = occurrencesList.get, reverse = True):
                print(f"[{page.getID():<5}] - (Relevância: {occurrencesList[page]}) - {page.getTitle():<55} ")
                # sortedList.append(page)
                
            # Printar lista de titulos ordenados por quantidade de ocorrência
            # for page in sortedList:
            #     print(f"{page.getID()} - {page.getTitle()}")
                
        except KeyError:
            print(f"[Palavra '{word}' não encontrada no hash]")
            
    def handleInput(self, input: str) -> str:
        # Passando para minúsculo todos os caracteres contidos na palavra
        input = input.lower()
        
        return input
        
    def printHash(self) -> None:
        for palavra in self.hash:
            print(f"indice[{palavra}]: {self.hash[palavra]}")

# busca = Search()
# busca.createHash()
# busca.searchByTitle("network")

# Tarefa 4
busca = Search()
busca.createHash_2()
busca.searchForRelevance("education")