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
driver.implicitly_wait(10)
driver.title

#### Find and create list of faction ids  #####

driver.find_element(By.ID, 'fac_901').click()  #clicks on the army
driver.implicitly_wait(10)
driver.find_element(By.ID, 'opcionSectorial_903').click()   #clicks on sectorial
driver.implicitly_wait(10)


###########################################################################################
###################     Executes inside sectorial page      ###############################
#########           Will run within loop for each sectorial         #######################
###################         Make this a function            ###############################
###########################################################################################

principal_panel = driver.find_element(By.ID, "contenedorLogosVertical")   #looks for the 'prinipal' panel where all the units are clickable
unit_list_panel = principal_panel.find_elements(By.CSS_SELECTOR, '.pastilla_logo_Unidad.ng-star-inserted')  #looks for list of units
unit_list = []
unit_list_info = []
clean_unit_list = []

#####   Get info from side panel    #####
for unit in unit_list_panel:
    unit_list.append(unit.get_attribute('id'))   #find the id of each unit to be clicked for more info
    unit_list_info.append(unit.text)             #takes all info from panel ()

for unit_char_list in unit_list_info:            #unit_list_info comes as (Type\nClassification\nName)
    clean_unit_list.append(unit_char_list.split('\n'))      #removes \n character and creates list of unit attributes

unit_type = []
unit_classification = []
unit_name = []
for unit_description in clean_unit_list:
    for i, element in enumerate(unit_description):
        if i%3 == 0:
            unit_type.append(element)
        elif i%3 == 1:
            unit_classification.append(element)
        elif i%3 == 2:
            unit_name.append(element)
        else:
            print('Not divisible by 3')

#####   Iterate through list of ids to open panel and gather data for each unit #####

principal_panel.find_element(By.ID, 'ryuken-unit-9').click()

## create dict, use name as key, list of all attributes
unit_panel = driver.find_element(By.ID, "panel_unidad")
unit_characteristics = []
try:
    unit_characteristics.append(unit_panel.find_element(By.XPATH, '//*[@id="caracteristicas_1"]/div[1]').get_attribute("title"))  # Cube
except:
    pass
try:
    unit_characteristics.append(unit_panel.find_element(By.XPATH, '//*[@id="caracteristicas_1"]/div[2]').get_attribute("title"))  # Order Type
except:
    pass
try:
    unit_characteristics.append(unit_panel.find_element(By.XPATH, '//*[@id="caracteristicas_1"]/div[3]').get_attribute("title"))  # Hackable
except:
    pass

# print(f'Unit types: {unit_type}')
# print(f'Unit classifications: {unit_classification}')
# print(f'Unit names: {unit_name}')
army_df = pd.DataFrame(list(zip(unit_name, unit_type, unit_classification)), columns = ['Name', 'Type', 'Classification'])
print(army_df)
army_df.to_csv('army_dataframe')

driver.quit()