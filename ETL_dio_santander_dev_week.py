'''To update, run: python.exe -m pip install --upgrade pip'''

# Documentação Oficial da API OpenAI: https://platform.openai.com/docs/api-reference/introduction
# Informações sobre o Período Gratuito: https://help.openai.com/en/articles/4936830

# Para gerar uma API Key:
# 1. Crie uma conta na OpenAI
# 2. Acesse a seção "API Keys"
# 3. Clique em "Create API Key"
# Link direto: https://platform.openai.com/account/api-keys


# OBJETIVO:
# Encontrar os clientes private com cartões de crédito
# os quais os limites são altos, não objetivando acessar
# os saldos das contas destes clientes private

import pandas as pd
import requests as r
import json as j
import openai as o
import random as rand

#################################################################
def get_all_data(url):
    response = r.get(f'{url}')
    return response.json() if response.status_code == 200 else None
#################################################################
#################################################################
def get_users(url,id_list):
    for id in id_list:
        response = r.get(f'{url}/users/{id}')
        return response.json() if response.status_code == 200 else None
#################################################################
#################################################################
def get_users_highlimit(data,limit):
    ids = []
    total = 0
    for d in data:
            if d['card'] is None or d['card']['limit'] is None:
                continue
            if d['card']['limit'] >= limit:
                ids.append(d)
                total += 1
    return ids, total
#################################################################
#################################################################
def get_symbol(symbol='USDBRL',interval=60,api_key='key'):
    market = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}min&outputsize=compact&apikey={api_key}'
    return market
#################################################################
#################################################################
def update_user(user,news):    
    user['news'].append({
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
        "description": news
    })
    response = r.put(f'{sdw2023_api_url}/{user}', json=user)
    return True if response.status_code == 200 else None
#################################################################
#################################################################
def get_users():
    response = r.get(f'{sdw2023_api_url}')
    return response.json() if response.status_code == 200 else None
#################################################################
#################################################################


###### EXTRAS ######
#df = pd.read_csv('SDW2023.csv')
#user_ids = df['UserID'].to_list()
#print(user_ids)

sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app/users'

########################################
# EXTRACTION
# search special clients (privates) with card limit > 5000000.0
########################################
# list all data clients
all_data_clients = get_users()
#print(j.dumps(all_data_clients, indent=2))

limit = 5000000.0 # 13 clients privates with 5 millions card limit
privates, total = get_users_highlimit(all_data_clients, limit)
#print(j.dumps(privates, indent=2))
print(f'Total clients: {total}')

# search the best moments for privates clients investmets application
symbol = 'AAPL'
intervalo = 60
api_key = 'H3Q84HT796E2J698'
alpha_vantage_api = get_symbol(symbol, intervalo, api_key)
# data market
data_market = get_all_data(alpha_vantage_api)
#print(j.dumps(data_market, indent=2))

'''parsed_data = j.loads(j.dumps(data_market["Time Series (60min)"], indent=2))
print(parsed_data)'''
volumes = []
for timestamp, data in data_market["Time Series (60min)"].items():
    volume = data["5. volume"]
    if int(volume) > 10000000:
        volumes.append(volume)
        print(f"Alerta de Preço: {timestamp}, Volume: {volume}")


########################################
#TRANSFORM / LOAD
# sending the best investments opportunities for all private clients
######################################## 
symbol = 'AAPL'
news = {
    1: f"Dica do candrelima: A {symbol} está em alta! É o momento perfeito para investir e colher os frutos de seu crescimento constante.",
    2: f"Dica do candrelima: O volume financeiro da {symbol} está nas alturas. Não perca a chance de investir em uma das gigantes da tecnologia.",
    3: f"Dica do candrelima: {symbol} é o ativo do momento, com um aumento significativo no volume de negociações. Siga a tendência e invista agora.",
    4: f"Dica do candrelima: A {symbol} está fazendo história com sua movimentação financeira. Torne-se parte desse sucesso investindo em {symbol}.",
    5: f"Dica do candrelima: {symbol} é sinônimo de inovação e crescimento. Aproveite a oportunidade e invista enquanto o volume financeiro está aquecido.",
    6: f"Dica do candrelima: A {symbol} está no centro das atenções com seu volume financeiro impressionante. Junte-se aos investidores inteligentes que já estão a bordo.",
    7: f"Dica do candrelima: O investimento em {symbol} está em alta demanda. Não espere mais, entre no mercado enquanto o volume financeiro é favorável.",
    8: f"Dica do candrelima: A {symbol} é uma escolha sólida com volume financeiro em ascensão. Invista agora e faça parte dessa jornada de sucesso.",
    9: f"Dica do candrelima: A {symbol} está decolando, e seu volume financeiro é um sinal claro. Não perca a chance de investir em uma empresa líder no setor de tecnologia.",
    10: f"Dica do candrelima: Com o aumento do volume financeiro, a {symbol} é a estrela do mercado. Invista hoje e acompanhe seu crescimento impressionante."
}
lista = [1,2,3,4,5,6,7,8,9,10]

# searching good opportunities for privates clients investments
# several news created by chatgpt prompt
# must complete update_put function with some news index (randomly)
for user in privates:
    print(j.dumps(user, indent=2))
    msg = rand.choice(lista)
    #print(news[msg])
    status = update_user(user, news[msg])
    if status:
        print(f'ID: {user} -> atualizado com as últimas notícias do {symbol}.')
