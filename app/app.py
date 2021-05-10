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
dadosAtualizadoAberturaCadaCincoMinutos = {}
dadosAtualizadoAberturaCadaDezMinutos = {}
minutoAnterior = -1


def obterPolinexApiDados():
    response = requests.get("https://poloniex.com/public?command=returnTicker")
    return response

def inicializarfechadurasCandles(key, value):
    global dadosAtualizadoAberturaCadaMinuto
    global dadosAtualizadoAberturaCadaCincoMinutos
    global dadosAtualizadoAberturaCadaDezMinutoe
   
    dadosAtualizadoAberturaCadaMinuto[key] = value['last']
    dadosAtualizadoAberturaCadaCincoMinutos[key] = value['last']
    dadosAtualizadoAberturaCadaDezMinutos[key] = value['last']
    
def atualizarDadosCadaSegundo():
    global dadosAtualizadoPorSegundo
    global minutoAnterior
    response = obterPolinexApiDados()
    if dadosAtualizadoPorSegundo == {}:
        for key, value in json.loads(response.text).items():
            dadosAtualizadoPorSegundo[key] = {'Open' : value['last'], 'Low': value['last'], 'High': value['last'], 'Close' : value['last']}
            inicializarfechadurasCandles(key, value)
    else:
        #Atualizando o maximo, o minimo e a fechadura a cada segundo para 
        #cada ativo
        for key, value in json.loads(response.text).items():
            if float(value['last']) > float(dadosAtualizadoPorSegundo[key]['High']):
                dadosAtualizadoPorSegundo[key]['High'] = value['last']		
            if float(value['last']) < float(dadosAtualizadoPorSegundo[key]['Low']):     dadosAtualizadoPorSegundo[key]['Low'] = value['last']	

            dadosAtualizadoPorSegundo[key]['Close'] = value['last']
                
        now = datetime.now()
        #print('datetime :', str(datetime.now()))
        if now.minute != minutoAnterior:
            minutoAnterior = now.minute
            salvarCandlesCadaMinuto(now)
                
def salvarCandlesCadaMinuto(now):
    global dadosAtualizadoPorSegundo
    global dadosAtualizadoAberturaCadaMinuto
    print("DateTime: ", str(now))
    print("1 Minuto :","Open: " +dadosAtualizadoAberturaCadaMinuto['BTC_BTS'] + " Low: " + dadosAtualizadoPorSegundo['BTC_BTS']['Low'] + " High: " + dadosAtualizadoPorSegundo['BTC_BTS']['High'] + " Close: "+ dadosAtualizadoPorSegundo['BTC_BTS']['Close'])
    #salvarCandlesNoBanco(1, dadosAtualizadoPorSegundo, dadosAtualizadoAberturaCadaMinuto, now)
    #Atualizando os dados de abertura a cada minuto para cada ativo
    for key, value in dadosAtualizadoAberturaCadaMinuto.items():
        value = dadosAtualizadoPorSegundo[key]['Close']
    if now.minute % 5 == 0:
        salvarCandlesCadaCincoMinutos(now)
    
def salvarCandlesCadaCincoMinutos(now):
    global dadosAtualizadoPorSegundo
    global dadosAtualizadoAberturaCadaCincoMinutos
    print("5 Minutos :","Open: " +dadosAtualizadoAberturaCadaCincoMinutos['BTC_BTS'] + " Low: " + dadosAtualizadoPorSegundo['BTC_BTS']['Low'] + " High: " + dadosAtualizadoPorSegundo['BTC_BTS']['High'] + " Close: "+ dadosAtualizadoPorSegundo['BTC_BTS']['Close'])
    #salvarCandlesNoBanco(5, dadosAtualizadoPorSegundo, dadosAtualizadoAberturaCadaCincoMinutos, now)
    #Atualizando os dados de abertura a cinco minutos para cada ativo
    for key, value in dadosAtualizadoAberturaCadaCincoMinutos.items():
        value = dadosAtualizadoPorSegundo[key]['Close']
    if now.minute % 10 == 0:
        salvarCandlesCadaDezMinutos(now)

def salvarCandlesCadaDezMinutos(now):
    global dadosAtualizadoPorSegundo
    global dadosAtualizadoAberturaCadaDezMinutos
    print("10 Minutos :","Open: " +dadosAtualizadoAberturaCadaDezMinutos['BTC_BTS'] + " Low: " + dadosAtualizadoPorSegundo['BTC_BTS']['Low'] + " High: " + dadosAtualizadoPorSegundo['BTC_BTS']['High'] + " Close: "+ dadosAtualizadoPorSegundo['BTC_BTS']['Close'])
    #salvarCandlesNoBanco(10, dadosAtualizadoPorSegundo, dadosAtualizadoAberturaCadaDezMinutos, now)
    #Atualizando os dados de abertura a Dez minutos para cada ativo
    for key, value in dadosAtualizadoAberturaCadaDezMinutos.items():
        value = dadosAtualizadoPorSegundo[key]['Close']

def salvarCandlesNoBanco(periodicidade, dadosAtualizados, dadosAbertura, now):
    for key, value in dadosAtualizados.items():
    #Inserindo Candles no Banco
        db.execute("Insert into candles (Moeda, Periodicidade ,Open,  Low, High, Close)" + " Values ("+
               str(key) + ',' +
               str(periodicidade) + ", "+   
               str(now) + ", " +  
               str(value['Open']) + "," + 
               str(value['Low']) + ","  + 
               str(value['High']) + "," + 
               str(value['Close']) + 
              ");")

if __name__ == '__main__':
    print('Application started')
    schedule.every().second.do(atualizarDadosCadaSegundo)
    while True:
        schedule.run_pending()
    print("Terminou!!!")
    



