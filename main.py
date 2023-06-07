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
            # Recupera as informações título e texto do XML
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
                # Passa todas as palavras que estiverem no plural para o singular
                word = self.toSingular(word)
                
                if word in self.hash:
                    # Adiciona o objeto da página em uma lista que está associada a uma posição do hash
                    self.hash[word].append(page)
                else:
                    # Cria uma lista associada a posição do hash e adiciona o primeiro objeto
                    self.hash[word] = []
                    self.hash[word].append(page)
            
    def searchByTitleOcurrences(self, word: str) -> None:
        # Passa todos os caracteres da palavra para minúsculo
        word = self.toLower(word)
        # Passa a palavra para o singular
        word = self.toSingular(word)
        occurrencesList = {}
        
        try:
            # Lista dos itens encontrados para a chave pesquisada
            pages = self.hash[word]
            
            # Guardando objeto como chave e quantidade de ocorrências como valor em itens de um dicionário
            for page in pages:
                title = page.getTitle()
                text = page.getText()
                
                occurrencesInTitle = title.count(word)
                occurrencesInText = text.count(word)
                
                # Verifica se existe alguma ocorrência da palavra no título
                if occurrencesInTitle > 0:
                    occurrences = occurrencesInText * 2
                else:
                    occurrences = occurrencesInText
                    
                occurrencesList[page] = occurrences

            # Criando uma lista com os objetos ordenados por quantidade de ocorrências em ordem decrescente
            print(f"{len(occurrencesList)} resultado(s) encontrado(s).")
            for page in sorted(occurrencesList, key = occurrencesList.get, reverse = True):
                print(f"[{page.getID():<5}] - (Relevância: {occurrencesList[page]:<3}) - {page.getTitle():<55} ")
                
        except KeyError:
            print(f"[ERRO]: Palavra '{word}' não encontrada no hash.")
            
    def toLower(self, input: str) -> str:
        # Passando para minúsculo todos os caracteres contidos na palavra
        input = input.lower()
        
        return input
    
    def toSingular(self, word: str) -> str:
        # Passa a palavra que está no plural para o singular
        lastLetterPos = len(word)-1
        lastLetter = word[lastLetterPos]
        singularWord = word[:lastLetterPos]
        
        # Se a palavra estiver no plural, retorna ela no singular. Senão, retorna a palavra original.
        if lastLetter == 's':
            return singularWord
        else:
            return word
    
    def menu(self) -> None:
        while(True):
            print("\x1b[2J\x1b[1;1H")
            word = input("Buscar pela palavra\n-> ")
            
            if len(word) < 4:
                print("[ERRO]: A palavra deve conter pelo menos 4 caracteres ou mais.")
            else:
                self.toSingular(word)
                self.searchByTitleOcurrences(word)
                
            input("Pressione ENTER para continuar...")
            continue
    
    def execute(self) -> None:
        self.createHash()
        self.menu()

search = Search()
search.execute()