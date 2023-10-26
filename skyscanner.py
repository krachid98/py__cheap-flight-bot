from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import re
import argparse
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
from fp.fp import FreeProxy
from selenium.webdriver.common.proxy import Proxy, ProxyType
import undetected_chromedriver as uc

#creo dizionario con le informazioni del volo, da dove parto a dove voglio arrivare e in quali dati
input_partenza = {
    'Departure': "MIL",
    'Arrival': "BCN",
    'Date': '30 marzo 2024'
}

input_ritorno = {
    'Departure': "VCE",
    'Arrival': "BCN",
    'Date': '30 marzo 2024'
}

def trova_volo_economico(informazioni_volo):
    
    PATH = r'"C:\Users\rachi\Documents\Karim\chromedriver\chromedriver-win32\chromedriver-win32\chromedriver.exe"'
    
    """
    #proxy ip dinamico
    proxy = FreeProxy(https=True).get()
    print('ok proxy: ' + proxy)
    
    # Configura il WebDriver di Selenium con il proxy
    options.add_argument(f'--proxy-server={proxy}')
    
    webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy": proxy,
        "ftpProxy": proxy,
        "sslProxy": proxy,
        "proxyType": "MANUAL",
    }
    
    webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True
    options.add_argument("user-agent="+user_agent)
    """
    
    options = webdriver.ChromeOptions()
        
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(options=options)
    
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    #vado al sito, in questo caso expedia
    driver.get("https://www.skyscanner.it/")
    
    time.sleep(50)
    
    #se blocca il bot...
    action = ActionChains(driver)
    element = driver.find_element((By.XPATH, '/html/body/div/div/div[2]/div[2]/p'))  # Sostituisci con l'ID dell'elemento desiderato
    action.context_click(element).perform()
    
    time.sleep(60)  # Tieni premuto il tasto destro del mouse per 5 secondi

    action.release().perform()  # Rilascia il tasto destro del mouse
    
    time.sleep(10)
    
    #go
    partenza = informazioni_volo['Departure']
    arrivo = informazioni_volo['Arrival']
    data = informazioni_volo['Date']
    
    time.sleep(2)
    
    #gestisco cookie
    elemento_cookie = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "acceptCookieButton"))
    )
    
    elemento_cookie.click()
    
    time.sleep(3)
    
    partenza_xpath = '//input[@aria-labelledby="originInput-label"]'
    partenza_field = WebDriverWait(driver, 8).until(
        EC.visibility_of_element_located((By.XPATH, partenza_xpath)))
    
    partenza_field.clear()
    partenza_field.click()
    partenza_field.send_keys(partenza)
    
    #arrivo
    arrivo_xpath = '//input[@aria-labelledby="destinationInput-label"]'
    arrivo_field = WebDriverWait(driver, 8).until(
        EC.visibility_of_element_located((By.XPATH, arrivo_xpath)))
    
    arrivo_field.clear()
    arrivo_field.click()
    arrivo_field.send_keys(arrivo)
    
    #voli diretti Voli diretti
    voliDiretti_xpath = '//input[@aria-label="Voli diretti"]'
    voliDiretti_field = WebDriverWait(driver, 8).until(
        EC.visibility_of_element_located((By.XPATH, voliDiretti_xpath)))
    
    voliDiretti_field.click()
    
    #data
    data_viaggio_xpath = '//button[contains(@aria-label, "{}")]'.format(data) #/.. cerca l'elemento padre cliccabile
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
            prossimo_mese_xpath = '//button[contains(@aria-label,"Prossimo mese")]'
            
            elem_prossimo_mese = WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.XPATH, prossimo_mese_xpath))
            )
            
            elem_prossimo_mese.click()
            time.sleep(1)
        
    #ho trovato la data e termino
    data_partenza_done = '//button[@data-testid="CalendarSearchButton"]'
    
    elem_data_partenza_done = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, data_partenza_done))
    )
    
    elem_data_partenza_done.click()
    
    #clicco cerca
    search_xpath = '//button[@data-testid="desktop-cta"]'
    
    elem_data_search = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, search_xpath))
    )
    
    elem_data_search.click()
    time.sleep(10)
    
trova_volo_economico(input_partenza)
    
    
    
    
    