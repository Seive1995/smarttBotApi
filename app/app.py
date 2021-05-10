import time
import random
import requests
import json
import schedule

from sqlalchemy import create_engine
from datetime import datetime

db_name = 'database'
db_user = 'username'
db_pass = 'secret'
db_host = 'db'
db_port = '5432'

# Connecto to the database
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)


dadosAtualizadoPorSegundo = {}
dadosAtualizadoAberturaCadaMinuto = {}
dadosAtualizadoMinimoCadaMinuto = {}
dadosAtualizadoMaximoCadaMinuto = {}
dadosAtualizadoFechaduraCadaMinuto = {}
dadosAtualizadoAberturaCadaCincoMinutos = {}
dadosAtualizadoMinimoCadaCincoMinutos = {}
dadosAtualizadoMaximoCadaCincoMinutos = {}
dadosAtualizadoFechaduraCadaCincoMinutos = {}
dadosAtualizadoAberturaCadaDezMinutos = {}
dadosAtualizadoMinimoCadaDezMinutos = {}
dadosAtualizadoMaximoCadaDezMinutos = {}
dadosAtualizadoFechaduraCadaDezMinutos = {}
minutoAnterior = -1


def obterPolinexApiDados():
    response = requests.get("https://poloniex.com/public?command=returnTicker")
    return response

def inicializarDados(key, value):
    global dadosAtualizadoAberturaCadaMinuto
    global dadosAtualizadoMinimoCadaMinuto
    global dadosAtualizadoMaximoCadaMinuto
    global dadosAtualizadoFechaduraCadaMinuto
    global dadosAtualizadoAberturaCadaCincoMinutos
    global dadosAtualizadoMinimoCadaCincoMinutos
    global dadosAtualizadoMaximoCadaCincoMinutos
    global dadosAtualizadoFechaduraCadaCincoMinutos
    global dadosAtualizadoAberturaCadaDezMinutos
    global dadosAtualizadoMinimoCadaDezMinutos
    global dadosAtualizadoMaximoCadaDezMinutos
    global dadosAtualizadoFechaduraCadaDezMinutos

   
    dadosAtualizadoAberturaCadaMinuto[key] = value['last'] 
    dadosAtualizadoMinimoCadaMinuto[key] = value['last']
    dadosAtualizadoMaximoCadaMinuto[key] = value['last']
    dadosAtualizadoFechaduraCadaMinuto[key] = value['last']
    dadosAtualizadoAberturaCadaCincoMinutos[key] = value['last']
    dadosAtualizadoMinimoCadaCincoMinutos[key] = value['last']
    dadosAtualizadoMaximoCadaCincoMinutos[key] = value['last']
    dadosAtualizadoFechaduraCadaCincoMinutos[key] = value['last']
    dadosAtualizadoAberturaCadaDezMinutos[key] = value['last']
    dadosAtualizadoMinimoCadaDezMinutos[key] = value['last']
    dadosAtualizadoMaximoCadaDezMinutos[key] = value['last']
    dadosAtualizadoFechaduraCadaDezMinutos[key] = value['last']

def resertarCandlesPorPeriodicidade(periodicidade,key, value):
    global dadosAtualizadoAberturaCadaMinuto
    global dadosAtualizadoMinimoCadaMinuto
    global dadosAtualizadoMaximoCadaMinuto
    global dadosAtualizadoFechaduraCadaMinuto
    global dadosAtualizadoAberturaCadaCincoMinutos
    global dadosAtualizadoMinimoCadaCincoMinutos
    global dadosAtualizadoMaximoCadaCincoMinutos
    global dadosAtualizadoFechaduraCadaCincoMinutos
    global dadosAtualizadoAberturaCadaDezMinutos
    global dadosAtualizadoMinimoCadaDezMinutos
    global dadosAtualizadoMaximoCadaDezMinutos
    global dadosAtualizadoFechaduraCadaDezMinutos

    if periodicidade == 1: 
        dadosAtualizadoAberturaCadaMinuto[key] = value['last']
        dadosAtualizadoMinimoCadaMinuto[key] = value['last']
        dadosAtualizadoMaximoCadaMinuto[key] = value['last']
        dadosAtualizadoFechaduraCadaMinuto[key] = value['last']
    
    if periodicidade == 5:
        dadosAtualizadoAberturaCadaCincoMinutos[key] = value['last']
        dadosAtualizadoMinimoCadaCincoMinutos[key] = value['last']
        dadosAtualizadoMaximoCadaCincoMinutos[key] = value['last']
        dadosAtualizadoFechaduraCadaCincoMinutos[key] = value['last']
    
    if periodicidade == 10:
        dadosAtualizadoAberturaCadaDezMinutos[key] = value['last']
        dadosAtualizadoMinimoCadaDezMinutos[key] = value['last']
        dadosAtualizadoMaximoCadaDezMinutos[key] = value['last']
        dadosAtualizadoFechaduraCadaDezMinutos[key] = value['last']


def atualizarDadosMinimo(key, value):
    global dadosAtualizadoMinimoCadaMinuto
    global dadosAtualizadoMinimoCadaCincoMinutos
    global dadosAtualizadoMinimoCadaDezMinutos

    if value['last'] < dadosAtualizadoMinimoCadaMinuto[key]:
        dadosAtualizadoMinimoCadaMinuto[key] = value['last']
    
    if value['last'] < dadosAtualizadoMinimoCadaCincoMinutos[key]:
        dadosAtualizadoMinimoCadaCincoMinutos[key] = value['last']

    if value['last'] < dadosAtualizadoMinimoCadaDezMinutos[key]:
        dadosAtualizadoMinimoCadaDezMinutos[key] = value['last']

def atualizarDadosMaximo(key, value):
    global dadosAtualizadoMaximoCadaMinuto
    global dadosAtualizadoMaximoCadaCincoMinutos
    global dadosAtualizadoMaximoCadaDezMinutos

    if value['last'] > dadosAtualizadoMaximoCadaMinuto[key]:
        dadosAtualizadoMaximoCadaMinuto[key] = value['last']

    if value['last'] > dadosAtualizadoMaximoCadaCincoMinutos[key]:
        dadosAtualizadoMaximoCadaCincoMinutos[key] = value['last']

    if value['last'] > dadosAtualizadoMaximoCadaDezMinutos[key]:
        dadosAtualizadoMaximoCadaDezMinutos[key] = value['last']
 
def atualizarDadosClose(key, value):
    global dadosAtualizadoFechaduraCadaMinuto
    global dadosAtualizadoFechaduraCadaCincoMinutos
    global dadosAtualizadoFechaduraCadaDezMinutos

    dadosAtualizadoFechaduraCadaMinuto[key] = value['last']
    dadosAtualizadoFechaduraCadaCincoMinutos[key] = value['last']
    dadosAtualizadoFechaduraCadaDezMinutos[key] = value['last']

def atualizarDados(key, value):
    atualizarDadosMinimo(key, value)
    atualizarDadosMaximo(key, value)
    atualizarDadosClose(key, value)
   
def atualizarDadosCadaSegundo():
    global dadosAtualizadoPorSegundo
    global minutoAnterior
    response = obterPolinexApiDados()
    if dadosAtualizadoPorSegundo == {}:
        dadosAtualizadoPorSegundo = json.loads(response.text)
        for key, value in json.loads(response.text).items():
            inicializarDados(key, value)
    else:
        #Atualizando o maximo, o minimo e a fechadura a cada segundo para 
        #cada ativo
        dadosAtualizadoPorSegundo = json.loads(response.text)
        for key, value in json.loads(response.text).items():
            atualizarDados(key, value)
                
        now = datetime.now()
        #print('datetime :', str(datetime.now()))
        if now.minute != minutoAnterior:
            minutoAnterior = now.minute
            salvarCandlesCadaMinuto(now)
                
def salvarCandlesCadaMinuto(now):
    global dadosAtualizadoPorSegundo
    global dadosAtualizadoAberturaCadaMinuto
    global dadosAtualizadoMinimoCadaMinuto
    global dadosAtualizadoMaximoCadaMinuto
    global dadosAtualizadoFechaduraCadaMinuto
    print("DateTime: ", str(now))
    print("1 Minuto :","Open: " + dadosAtualizadoAberturaCadaMinuto['BTC_BTS'] + " Low: " + dadosAtualizadoMinimoCadaMinuto['BTC_BTS'] + " High: " + dadosAtualizadoMaximoCadaMinuto['BTC_BTS'] + " Close: "+ dadosAtualizadoFechaduraCadaMinuto['BTC_BTS'])
    salvarCandlesNoBanco(1, dadosAtualizadoAberturaCadaMinuto, dadosAtualizadoMinimoCadaMinuto, dadosAtualizadoMaximoCadaMinuto, dadosAtualizadoFechaduraCadaMinuto, now)
    #Resertando  dados de candles de 1 min de cada ativo para seus preços atuais.
    for key, value in dadosAtualizadoPorSegundo.items():
        resertarCandlesPorPeriodicidade(1, key, value)    
    if now.minute % 5 == 0:
        salvarCandlesCadaCincoMinutos(now)
    
def salvarCandlesCadaCincoMinutos(now):
    global dadosAtualizadoPorSegundo
    global dadosAtualizadoAberturaCadaCincoMinutos
    global dadosAtualizadoMinimoCadaCincoMinutos
    global dadosAtualizadoMaximoCadaCincoMinutos
    global dadosAtualizadoFechaduraCadaCincoMinutos

    print("5 Minuto :","Open: " + dadosAtualizadoAberturaCadaCincoMinutos['BTC_BTS'] + " Low: " + dadosAtualizadoMinimoCadaCincoMinutos['BTC_BTS'] + " High: " + dadosAtualizadoMaximoCadaCincoMinutos['BTC_BTS'] + " Close: "+ dadosAtualizadoFechaduraCadaCincoMinutos['BTC_BTS'])
    salvarCandlesNoBanco(5, dadosAtualizadoAberturaCadaCincoMinutos, dadosAtualizadoMinimoCadaCincoMinutos, dadosAtualizadoMaximoCadaCincoMinutos, dadosAtualizadoFechaduraCadaCincoMinutos, now)
    #Resertando dados de candles de 5 minutos de cada ativo para seus preços atuais
    for key, value in dadosAtualizadoPorSegundo.items():
        resertarCandlesPorPeriodicidade(5, key, value)            
    if now.minute % 10 == 0:
        salvarCandlesCadaDezMinutos(now)

def salvarCandlesCadaDezMinutos(now):
    global dadosAtualizadoPorSegundo
    global dadosAtualizadoAberturaCadaDezMinutos
    global dadosAtualizadoMinimoCadaDezMinutos
    global dadosAtualizadoMaximoCadaDezMinutos
    global dadosAtualizadoFechaduraCadaDezMinutos

    print("10 Minuto :","Open: " + dadosAtualizadoAberturaCadaDezMinutos['BTC_BTS'] + " Low: " + dadosAtualizadoMinimoCadaDezMinutos['BTC_BTS'] + " High: " + dadosAtualizadoMaximoCadaDezMinutos['BTC_BTS'] + " Close: "+ dadosAtualizadoFechaduraCadaDezMinutos['BTC_BTS'])

    salvarCandlesNoBanco(10, dadosAtualizadoAberturaCadaDezMinutos, dadosAtualizadoMinimoCadaDezMinutos, dadosAtualizadoMaximoCadaDezMinutos, dadosAtualizadoFechaduraCadaDezMinutos, now)
    #Resertando dados de candles de 10 min de cada ativo para seus preços atuais
    for key, value in dadosAtualizadoPorSegundo.items():
        resertarCandlesPorPeriodicidade(10, key, value)    
    
def salvarCandlesNoBanco(periodicidade, dadosAbertura, dadosMinimo, dadosMaximo, dadosFechadura, now):
    global dadosAtualizadoPorSegundo
    for key, value in dadosAtualizadoPorSegundo.items():
    #Inserindo Candles no Banco
        db.execute("Insert into candles (Moeda, Periodicidade, Date_time, Open,  Low, High, Close)" + " Values ("+
               str(key) + ',' +
               str(periodicidade) + ", "+   
               str(now) + ", " +  
               str(dadosAbertura[key]) + "," + 
               str(dadosMinimo[key]) + ","  + 
               str(dadosMaximo[key]) + "," + 
               str(dadosFechadura[key]) + 
              ");")

if __name__ == '__main__':
    print('Application started')
    schedule.every().second.do(atualizarDadosCadaSegundo)
    while True:
        schedule.run_pending()
    print("Terminou!!!")
    



