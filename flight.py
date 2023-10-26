from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import re

import sys

from selenium.common.exceptions import TimeoutException
import time

import pandas as pd

import smtplib
from email.message import EmailMessage

import schedule
from _ast import Try
from selenium.common.exceptions import TimeoutException
from django.conf.locale import ms
from selenium.webdriver.common.devtools.v113.target import send_message_to_target
from sched import scheduler

print('ciaso')

#creo dizionario con le informazioni del volo, da dove parto a dove voglio arrivare e in quali dati
input_partenza = {
    'Departure': "VCE",
    'Arrival': "BCN",
    'Date': '30 marzo 2024'
}

input_ritorno = {
    'Departure': "VRN",
    'Arrival': "BCN",
    'Date': '30 marzo 2024'
}

def trova_volo_economico(informazioni_volo):
    
    PATH = r'"C:\Users\rachi\Documents\Karim\chromedriver\chromedriver-win32\chromedriver-win32\chromedriver.exe"'

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--start-maximized")
    
    '''
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument('--window-size=1920,1080')
    '''
    
    driver = webdriver.Chrome(options=options)
    
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
    
    partenza = informazioni_volo['Departure']
    arrivo = informazioni_volo['Arrival']
    data = informazioni_volo['Date']
    
    #vado al sito, in questo caso expedia
    driver.get("https://www.expedia.it")
    
    time.sleep(2)
    
    #gestisco cookie
    elemento_cookie = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "osano-cm-denyAll"))
    )
    
    elemento_cookie.click()
    
    time.sleep(3)
    
    #clicco sezione 'Voli'
    #print("Sez---Voli")
    
    voli_xpath = '//a[@href="/Flights"]'
    elemento_voli = WebDriverWait(driver, 100).until(
        EC.visibility_of_element_located((By.XPATH, voli_xpath))
    )
    
    #print(elemento_voli)
    
    elemento_voli.click()
    
    time.sleep(0.2)
    
    #vado solo con viaggi di sola andata/ritorno
    sola_andata = '//a[@aria-controls="FlightSearchForm_ONE_WAY"]'
    elemento_sola_andata = WebDriverWait(driver, 8).until(
        EC.visibility_of_element_located((By.XPATH, sola_andata))
    )
    
    elemento_sola_andata.click()
    time.sleep(0.2)
    
    #prima parte: partenza, ritorno, data partenza e data arrivo
    partenza_xpath = '//button[contains(@aria-label, "Partenza")]'
    
    elemento_partenza = WebDriverWait(driver, 100).until(
        EC.visibility_of_element_located((By.XPATH, partenza_xpath))
    )
    
    #elemento_partenza = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, partenza_xpath))).send_keys("Programming")
    
    #elem_partenza = driver.find_element(By.XPATH, partenza_xpath)
    
    elemento_partenza.clear
    elemento_partenza.click()
        
    time.sleep(1)
    
    #print(partenza)
    
    elem_partenza = driver.find_element(By.XPATH, '//input[@id="origin_select"]')
    
    elem_partenza.send_keys(partenza)
    
    time.sleep(1)
    
    elem_partenza.send_keys(Keys.ENTER)
    
    time.sleep(0.5)
    
    #comincio parte destinazione
    destinazione_xpath = '//button[contains(@aria-label, "Destinazione")]'
    elemento_destinazione = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, destinazione_xpath))
    )
    
    elemento_destinazione.clear
    elemento_destinazione.click()
    time.sleep(1)
    
    elem_destinazione = driver.find_element(By.XPATH, '//input[@id="destination_select"]')
    
    elem_destinazione.send_keys(arrivo)
    
    time.sleep(1)
    elem_destinazione.send_keys(Keys.ENTER)
    
    #completo parte riguardo alla data
    data_partenza_xpath = '//button[contains(@aria-label, "Data")]'
    elemento_data_partenza = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, data_partenza_xpath))
    )
    
    elemento_data_partenza.click()
    time.sleep(2)
    
    #trovo data corrente
    data_viaggio_xpath = '//div[contains(@aria-label, "{}")]/..'.format(data) #/.. cerca l'elemento padre cliccabile
    print(data_viaggio_xpath)
    elemento_data_viaggio = ""
    
    while elemento_data_viaggio ==  "":
        try:
            elemento_data_viaggio = WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.XPATH, data_viaggio_xpath))
                )
            elemento_data_viaggio.click()
        
        except TimeoutException:
            elemento_data_viaggio = ""
        
            #passo al prossimo mese e vedo se corrisponde con quello che sceglie l'utente
            prossimo_mese_xpath = '//button[@data-stid="uitk-calendar-navigation-controls-next-button"]'
            
            elem_prossimo_mese = WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.XPATH, prossimo_mese_xpath))
            )
            
            elem_prossimo_mese.click()
            time.sleep(1)
        
    #ho trovato la data e termino
    data_partenza_done = '//button[@data-stid="apply-date-selector"]'
    
    elem_data_partenza_done = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, data_partenza_done))
    )
    
    elem_data_partenza_done.click()
    
    #clicco cerca
    search_xpath = '//button[@id="search_button"]'
    
    elem_data_search = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, search_xpath))
    )
    
    elem_data_search.click()
    time.sleep(10)
    
    #comincio parte filtri, check prezzi ed invio mail
    voli_diretti_xpath = '//input[contains(@aria-label, "voli diretti")]'
    voli_uno_scalo_xpath  ='//input[contains(@aria-label, "voli 1 scalo")]'
    
    if len(driver.find_elements(By.XPATH, voli_diretti_xpath)) > 0: #se la checkbox è presente la clicco
        driver.find_element(By.XPATH, voli_diretti_xpath).click()
        time.sleep(5)
        
        #vedo se ci sono voli disponibili verificando uno span nascosto dietro ogni riga di risultato
        voli_disponibili = driver.find_elements(By.XPATH, '//span[contains(text(), "Seleziona e visualizza le informazioni tariffarie")]')
        voli = []
        
        if len(voli_disponibili) > 0:
            if len(voli_disponibili) == 1: #un risultato, non serve che ordino i risultati per prezzo
                '''
                voli = [(item.text.split(",")[0].split("per")[-1].title(),
                         item.text.split(",")[1].title().replace("alle", ":"),
                         item.text.split(",")[2].title().replace("alle", ":"),
                         item.text.split(",")[3].title().replace("alle", ":")) for item in voli_disponibili[0:5]] #recupero i primi 5 risultati ordinati per prezzo
                '''
                
                # Utilizza espressioni regolari per estrarre le informazioni desiderate
                for stringa in voli_disponibili:
                    compagnia = re.search(r'volo (.+?) con', stringa.text).group(1)
                    
                    codice_xpath = '//div[@data-test-id="arrival-departure"]';
                    codice = driver.find_element(By.XPATH, codice_xpath).text
                    
                    codici = re.findall(r'\((.*?)\)', codice)
                    codice_partenza = codici[0]
                    codice_arrivo = codici[1]
                    
                    partenza = re.search(r'partenza alle ore (.+?) da (.+?),', stringa.text)
                    arrivo = re.search(r'in arrivo alle ore (.+?) a (.+?),', stringa.text)
                    prezzo = re.search(r'con prezzo pari a (.+?),', stringa.text).group(1)
                    
                    prezzoNew = prezzo.replace(' Solo andata', '')
                    
                    # Crea un dizionario con le informazioni
                    voli.append({
                        'Compagnia': compagnia,
                        'Partenza': f"{partenza.group(1)} da {partenza.group(2)} ({codice_partenza})",
                        'Arrivo': f"{arrivo.group(1)} a {arrivo.group(2)} ({codice_arrivo})",
                        'Prezzo': prezzoNew
                    })
            else:
                #qui devo ordinare per prezzo
                #prezzo_decrescente = driver.find_elements(By.XPATH, '//option[@data-opt-id="PRICE_INCREASING"]').click()
                
                select_element = driver.find_element(By.NAME, 'SORT')
                # Utilizza Select per interagire con l'elemento select
                selectElement = Select(select_element)
                # Imposta il valore dell'option
                selectElement.select_by_value('PRICE_INCREASING')

                #sleep
                time.sleep(5)
                '''
                voli = [(item.text.split(",")[0].split("per")[-1].title(),
                         item.text.split(",")[1].title().replace("alle", ":"),
                         item.text.split(",")[2].title().replace("alle", ":"),
                         item.text.split(",")[3].title().replace("alle", ":")) for item in voli_disponibili[0:5]] #recupero i primi 5 risultati ordinati per prezzo
                '''
                
                # Utilizza espressioni regolari per estrarre le informazioni desiderate
                for stringa in voli_disponibili:
                    compagnia = re.search(r'volo (.+?) con', stringa.text).group(1)
                    
                    codice_xpath = '//div[@data-test-id="arrival-departure"]';
                    codice = driver.find_element(By.XPATH, codice_xpath).text
                    
                    codici = re.findall(r'\((.*?)\)', codice)
                    codice_partenza = codici[0]
                    codice_arrivo = codici[1]

                    partenza = re.search(r'partenza alle ore (.+?) da (.+?),', stringa.text)
                    arrivo = re.search(r'in arrivo alle ore (.+?) a (.+?),', stringa.text)
                    prezzo = re.search(r'con prezzo pari a (.+?),', stringa.text).group(1)
                    
                    prezzoNew = prezzo.replace(' Solo andata', '')
                    
                    # Crea un dizionario con le informazioni
                    voli.append({
                        'Compagnia': compagnia,
                        'Partenza': f"{partenza.group(1)} da {partenza.group(2)} ({codice_partenza})",
                        'Arrivo': f"{arrivo.group(1)} a {arrivo.group(2)} ({codice_arrivo})",
                        'Prezzo': prezzoNew
                    })

            print("Condizioni soddisfatte per: {}:{}, {}:{}, {}:{}".format("Departure", partenza, "Arrivo", arrivo, "Data", data))
                      
            #il bot termina qui
            driver.quit()
                
            return voli
        
        else:
            print("Condizioni non soddisfatte per: {}:{}, {}:{}, {}:{}".format("Departure", partenza, "Arrivo", arrivo, "Data", data))
            
            #termino
            driver.quit()
            
            return []
    else:
        print("Non ho trovato voli diretti!")
        
        return []


def send_email():
    andata = trova_volo_economico(input_partenza)
    ritorno = trova_volo_economico(input_ritorno)
    
    #inserisco tutto in un dataframe in modo da rendere la visualizzazione più easy
    dataFrame = pd.DataFrame(andata + ritorno) #+ ritorno al momento commentato perchè ho bisogno solo dell'andata

    if not dataFrame.empty: #mando email solo se ho delle informazioni del volo
        email = open(r'Email.txt').read()
        password = open(r'Password.txt').read()
        
        msg = EmailMessage()
        
        msg["Subject"] = "Python Informazioni Volo! {} --> {}, Partenza: {}, Ritorno: {}".format(input_partenza['Departure'], input_partenza['Arrival'], input_partenza['Date'], input_ritorno['Date'])
        msg["From"] = email
        msg["To"] = email
        
        msg.add_alternative("""\
            <!DOCTYPE html>
            <html>
                <body>
                    {}
                </body>
            </html>""".format(dataFrame.to_html()), subtype="html")
        
        #da sistemare SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email, password)
            smtp.send_message(msg)

send_email()

#eseguo
schedule.clear()
schedule.every(60).minutes.do(send_email)

while True:
    schedule.run_pending()
    time.sleep(1)
    
    
    
    
    