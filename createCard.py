import requests
from credenciais import APIKey, APIToken # Crie um arquivo com suas credenciais
from cardsConfig import LISTA_OS, LISTA_EMANDAMENTO, LISTA_NOVENTADIAS, LISTA_CONCLUIDO, LISTA_CONEXOES
from dbConnector import OSinfo

#IDs de etiquetas do Trello
prioridade = {
    'E': '65d78722920b46a0e96232fc',
    'A': '65d7af9379a1397c7d16e11d',
    'M': '65d7b101fa0d844893d8a326',
    'B': '65d78722920b46a0e96232f5',
    'U': '65d78722920b46a0e96232fa'
}
# ID da etiqueta para OS com Número Philips
NR_PHILIPS = '65e7aee56bb74f4eebade490'

# URL base para a API do Trello
URL = "https://api.trello.com/1/cards"

# Obtendo informações das OS
results = OSinfo()

# Função para buscar cards
def fetch_cards_from_list(list_id):
    lista_cards_url = f"https://api.trello.com/1/lists/{list_id}/cards"
    lista_cards_response = requests.get(lista_cards_url, params={'key': APIKey, 'token': APIToken})
    #Tratamento de erro ao consultar os Cards
    try:
        lista_cards_response.raise_for_status() 
        return lista_cards_response.json()
    except requests.exceptions.HTTPError as err_http:
        print(f"Erro HTTP ao buscar cartões da lista: {err_http}")
        return []
    except requests.exceptions.RequestException as err_req:
        print(f"Ocorreu um erro inesperado ao buscar cartões da lista: {err_req}")
        return []

# Obtendo cards de todas as listas
all_cards_data = {}
for lista_id in [LISTA_OS, LISTA_EMANDAMENTO, LISTA_NOVENTADIAS, LISTA_CONCLUIDO, LISTA_CONEXOES]:
    all_cards_data[lista_id] = fetch_cards_from_list(lista_id)

for title, philips, dt_inicio, dt_fim, prio in results:
    label_id = []
    
    # Verificando se existe Número Philips na OS
    if philips is not None:
        label_id.append(NR_PHILIPS)
    
    # Verificando a prioridade da OS
    if prio in prioridade:
        label_id.append(prioridade[prio])
    
    # Verificando se o cartão já existe em alguma lista
    card_exists = False

    for lista_id, cards in all_cards_data.items():
        if any(card['name'] == title for card in cards):
            card_exists = True
            print(f"O cartão com o nome '{title}' já existe na lista {lista_id}. Não será criado novamente.")
            break
    
    if not card_exists:
        # Direcionando as OS para seus Cards
        if dt_inicio is None and dt_fim is None:
            idList = LISTA_OS
        elif dt_inicio is not None and dt_fim is None:
            idList = LISTA_EMANDAMENTO
        elif dt_inicio is not None and dt_fim is not None:
            diff_dias = (dt_fim - dt_inicio).days
            if diff_dias >= 90:
                idList = LISTA_NOVENTADIAS
            else:
                idList = LISTA_CONCLUIDO
        
        headers = {"Accept": "application/json"}
        query = {
            'idList': idList,
            'key': APIKey,
            'token': APIToken,
            'name': title,
            'idLabels': label_id
        }
        
        # Enviando uma solicitação POST para criar o cartão
        response = requests.request("POST", URL, headers=headers, params=query)

        #Tratamento de erro ao criar o Card
        try:
            response.raise_for_status()  
        except requests.exceptions.HTTPError as err_http:
            print(f"Erro HTTP ao criar cartão: {err_http}")
        except requests.exceptions.RequestException as err_req:
            print(f"Ocorreu um erro inesperado ao criar cartão: {err_req}")
