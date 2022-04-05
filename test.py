from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd

# Establish chrome driver and go to report site URL
url = "https://infinitytheuniverse.com/army/infinity"
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(0.5)
driver.title

#### Find and create list of faction ids  #####
faction_id_driver = driver.find_elements(By.CSS_SELECTOR, '.logo_faccion.desactivo.ng-star-inserted')  # find all elements of factions
faction_sectorial_dict = {}
for fact_id in faction_id_driver:
    faction_sectorial_dict[fact_id.get_attribute('id')] = [[],[]]  # create a key of current faction with 2 lists


for fact in faction_sectorial_dict:
    #print(f'Faction: {fact}')
    driver.find_element(By.ID, fact).click()  # click on current faction
    driver.implicitly_wait(0.5)
    sectorial_selection_driver = driver.find_elements(By.CSS_SELECTOR, '.panel_sectorial.ng-star-inserted')  # find all elements of each sectorial
    sectorial_selection_list = []
    for sect in sectorial_selection_driver:   # run through all the elements of sectorials
        faction_sectorial_dict[fact][0].append(sect.get_attribute('id'))  # add the id of the sectorials into the first list of the factions key
    sect_panel = driver.find_element(By.ID, 'sectoriales')   # find the sectorial panel 
    for sect_id in faction_sectorial_dict[fact][0]:     # iterate through the sectorial ids
        sectorial_section = sect_panel.find_element(By.ID, sect_id)
        faction_sectorial_dict[fact][1].append(sectorial_section.find_element(By.CLASS_NAME, 'nombre_sectorial').text)  # collect the names of all the sectorials in the current faction

#print(faction_sectorial_dict)

for fact, sect in faction_sectorial_dict.items():
    #print(f'Key: {fact}\nValue: {sect}')
    for sectorial in sect[0]:
        #print(f'Sectorial: {sectorial}')
        driver.get(url)
        driver.find_element(By.ID, fact).click()
        driver.find_element(By.ID, sectorial).click()










driver.quit()