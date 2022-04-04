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

driver.find_element(By.ID, 'fac_901').click()  #clicks on the army
driver.implicitly_wait(0.5)
driver.find_element(By.ID, 'opcionSectorial_903').click()   #clicks on sectorial
driver.implicitly_wait(0.5)


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
unit_characteristics = {}

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
for unit in unit_list:
    principal_panel.find_element(By.ID, unit).click()

    ## create dict, use name as key, list of all attributes
    unit_panel = driver.find_element(By.ID, "panel_unidad")
    unit_attributes = driver.find_element(By.CLASS_NAME, 'barra_atributos')
    unit_characteristics[unit_panel.find_element(By.ID, 'perfil1_nombre').text] = [[],[],[],[]]

    try:
        unit_characteristics[unit_panel.find_element(By.ID, 'perfil1_nombre').text][0].append(unit_panel.find_element(By.XPATH, '//*[@id="caracteristicas_1"]/div[1]').get_attribute("title"))  # Cube
    except:
        pass
    try:
        unit_characteristics[unit_panel.find_element(By.ID, 'perfil1_nombre').text][0].append(unit_panel.find_element(By.XPATH, '//*[@id="caracteristicas_1"]/div[2]').get_attribute("title"))  # Order Type
    except:
        pass
    try:
        unit_characteristics[unit_panel.find_element(By.ID, 'perfil1_nombre').text][0].append(unit_panel.find_element(By.XPATH, '//*[@id="caracteristicas_1"]/div[3]').get_attribute("title"))  # Hackable
    except:
        pass
    try:
        unit_characteristics[unit_panel.find_element(By.ID, 'perfil1_nombre').text][0].append(unit_panel.find_element(By.XPATH, '//*[@id="caracteristicas_1"]/div[4]').get_attribute("title"))  # Hackable
    except:
        pass
    try:
        all_attributes = unit_attributes.find_elements(By.CLASS_NAME, 'valor')
        for attr in all_attributes:
            unit_characteristics[unit_panel.find_element(By.ID, 'perfil1_nombre').text][1].append(attr.text)  # All attributes (MOV, CC, BS, etc...)
    except:
        pass
    try:
        equip_list_element = unit_panel.find_element(By.ID, 'lista_equipo1')
        unit_characteristics[unit_panel.find_element(By.ID, 'perfil1_nombre').text][2].append(equip_list_element.text)  # Equipment
    except:
        pass
    try:
        special_list_element = unit_panel.find_element(By.ID, 'lista_habilidades1')
        unit_characteristics[unit_panel.find_element(By.ID, 'perfil1_nombre').text][3].append(special_list_element.text)  # Special Skills \n•\n
    except:
        pass

unit_mov = []
unit_cc = []
unit_bs = []
unit_ph = []
unit_wip = []
unit_arm = []
unit_bts = []
unit_w = []
unit_s = []
unit_ava = []
unit_equip = []
unit_special = []
unit_characteristics_list = []


for value in unit_characteristics.values():
    unit_mov.append(value[1][0])
    unit_cc.append(value[1][1])
    unit_bs.append(value[1][2])
    unit_ph.append(value[1][3])
    unit_wip.append(value[1][4])
    unit_arm.append(value[1][5])
    unit_bts.append(value[1][6])
    unit_w.append(value[1][7])
    unit_s.append(value[1][8])
    unit_ava.append(value[1][9])
    try:
        value[2] = value[2][0].split('\n•\n')
    except:
        pass
    try:
        value[3] = value[3][0].split('\n•\n')
    except:
        pass
    unit_equip.append(value[2])
    unit_special.append(value[3])
    unit_characteristics_list.append(value[0])


print(f'Unit characteristics dict: {unit_characteristics}')


army_df = pd.DataFrame(list(zip(unit_name, unit_type, unit_classification, unit_mov, unit_cc, unit_bs, unit_ph, unit_wip, unit_arm, unit_bts, unit_w, unit_s, unit_ava, unit_equip, unit_special, unit_characteristics_list)), columns = ['Name', 'Type', 'Classification', 'MOV', 'CC', 'BS', 'PH', 'WIP', 'ARM', 'BTS', 'W', 'S', 'AVA', 'Equipment', 'Special Skills', 'Characteristics'])
print(army_df)
army_df.to_csv('army_dataframe')

driver.quit()