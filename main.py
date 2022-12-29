import os 
import time as t
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    UnexpectedAlertPresentException,
    NoSuchElementException)



def adaptar_item(item):
    if item < 10:
        
        return '0' + str(item)
    else:
        return item  


def hora_setup():
    
    data_atual = t.localtime()
    ano, mes, dia, hora, minuto, seg, dia_semana, dia_ano, isdst = data_atual
    return f'{adaptar_item(dia)}{adaptar_item(mes)}-{adaptar_item(hora)}{adaptar_item(minuto)}{adaptar_item(seg)}'


def definir_topicos(maximo: int, nomes_pesquisa: list = []) -> tuple:
    '''
    Nesta função, o objetivo da mesma é, como primeiro argumento, passar a quantidade máxima por cada tópico buscar os links.\n
    Como segundo argumento, uma lista contendo os tópicos de pesquisa (Não há limite de tópicos
    '''
    return len(nomes_pesquisa), nomes_pesquisa, maximo



### drive do navegador
servico = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless')
drive = webdriver.Chrome(service=servico, options=options)
drive.maximize_window()

marktime = WebDriverWait(drive, 90)


quantidade, lista_topicos, quantidade_maxima_por_topico = definir_topicos(10, ['python','comida','música'])

###### Exercutar

lista_videos_objeto = []
dados = {}
for i, item in enumerate(lista_topicos):
    drive.get(f'https://youtube.com/results?search_query={item}')
    
    marktime.until(
        EC.presence_of_element_located(
            (By.ID, 'thumbnail')
        )
    )
    
    t.sleep(2)
    
    
    info = drive.find_elements(By.ID, 'dismissible')[:quantidade_maxima_por_topico]
 

    links = [item.find_element(By.ID, 'thumbnail').get_attribute('href') for item in info]
    
    with open(f'Links-{lista_topicos[i]}.{hora_setup()}', 'w') as f:
        
        f.write('\n'.join(links))

    info = {lista_topicos[i]: links}
    dados.update(info)
    
print(dados)
    