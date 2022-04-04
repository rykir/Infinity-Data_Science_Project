###########################################################################################################################
###################     See https://www.infinitytheacademy.com/basic/reading-profiles/      ###############################
###################                         for infinity explaination                       ###############################
###################                                                                         ###############################
###########################################################################################################################


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
faction_id_driver = driver.find_elements(By.CSS_SELECTOR, '.logo_faccion.desactivo.ng-star-inserted')
faction_sectorial_dict = {}
for fact_id in faction_id_driver:
    faction_sectorial_dict[fact_id.get_attribute('id')] = [[],[]]


for fact in faction_sectorial_dict:
    driver.find_element(By.ID, fact).click()
    driver.implicitly_wait(0.5)
    sectorial_selection_driver = driver.find_elements(By.CSS_SELECTOR, '.panel_sectorial.ng-star-inserted')
    sectorial_selection_list = []
    for sect in sectorial_selection_driver:
        faction_sectorial_dict[fact][0].append(sect.get_attribute('id'))
    sect_panel = driver.find_element(By.ID, 'sectoriales')    
    for sect_id in faction_sectorial_dict[fact][0]:
        sectorial_section = sect_panel.find_element(By.ID, sect_id)
        faction_sectorial_dict[fact][1].append(sectorial_section.find_element(By.CLASS_NAME, 'nombre_sectorial').text)














driver.quit()