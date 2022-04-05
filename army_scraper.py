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


def faction_sectorial_list():
    #### Find and create list of faction ids  #####
    faction_id_driver = driver.find_elements(By.CSS_SELECTOR, '.logo_faccion.desactivo.ng-star-inserted')  # find all elements of factions
    faction_sectorial_dict = {}
    for fact_id in faction_id_driver:
        faction_sectorial_dict[fact_id.get_attribute('id')] = [[],[]]  # create a key of current faction with 2 lists


    for fact in faction_sectorial_dict:
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
    return faction_sectorial_dict



###########################################################################################
###################     Executes inside sectorial page      ###############################
#########           Will run within loop for each sectorial         #######################
###########################################################################################
def collect_army_data(sect_name):
    principal_panel = driver.find_element(By.ID, "contenedorLogosVertical")   #looks for the 'prinipal' panel where all the units are clickable
    unit_list_panel = principal_panel.find_elements(By.CSS_SELECTOR, '.pastilla_logo_Unidad.ng-star-inserted')  #looks for list of units
    unit_list = []
    unit_list_info = []
    clean_unit_list = []
    sectorial_list = []

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
    sub_units = {}

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
        sectorial_list.append(sectorial)
        unit_panel = driver.find_element(By.ID, "panel_unidad")
        unit_attributes = driver.find_element(By.CLASS_NAME, 'barra_atributos')
        unit_characteristics[unit_panel.find_element(By.ID, 'perfil1_nombre').text] = [[],[],[],[]]
        sub_unit_panel = unit_panel.find_element(By.ID, 'contenedor_opciones')
        sub_ids = sub_unit_panel.find_elements(By.CSS_SELECTOR, '.linea_opcion.clearfix.ng-star-inserted')  #get the ids of all the subunits
        

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
        try:
            for sub_id in sub_ids:
                #print(f'Sub id: {sub_id.find_element(By.CLASS_NAME, 'nombre').text}')
                sub_units[sub_id.find_element(By.CLASS_NAME, 'nombre').text] = [] # Create dict for sub units, weaps, melee, swc, c
                sub_units[sub_id.find_element(By.CLASS_NAME, 'nombre').text].append(sub_id.find_element(By.CLASS_NAME, 'armasCD').text)
                sub_units[sub_id.find_element(By.CLASS_NAME, 'nombre').text].append(sub_id.find_element(By.CLASS_NAME, 'armasCC').text)
                sub_units[sub_id.find_element(By.CLASS_NAME, 'nombre').text].append(sub_id.find_element(By.CLASS_NAME, 'cap').text)
                sub_units[sub_id.find_element(By.CLASS_NAME, 'nombre').text].append(sub_id.find_element(By.CLASS_NAME, 'c').text)
                sub_units[sub_id.find_element(By.CLASS_NAME, 'nombre').text].append(unit_panel.find_element(By.ID, 'perfil1_nombre').text)
        except:
            print('No sub id')
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

    army_df = pd.DataFrame(list(zip(unit_name, sectorial_list, unit_type, unit_classification, unit_mov, unit_cc, unit_bs, unit_ph, unit_wip, unit_arm, unit_bts, unit_w, unit_s, unit_ava, unit_equip, unit_special, unit_characteristics_list)), columns = ['Name', 'Sectorial', 'Type', 'Classification', 'MOV', 'CC', 'BS', 'PH', 'WIP', 'ARM', 'BTS', 'W', 'S', 'AVA', 'Equipment', 'Special Skills', 'Characteristics'])
    print(army_df)
    sub_df = pd.DataFrame.from_dict(sub_units, orient='index', columns=['Weapon(s)', 'Melee Weapons', 'SWC', 'C', 'Base Name'])
    sub_df.to_csv(f'{sect_name}_sub-units_dataframe')
    army_df.to_csv(f'{sect_name}_dataframe')

    return 

faction_sectorial_dict = faction_sectorial_list()

"""
for fact, sect in faction_sectorial_dict.items():
    for sectorial in sect[0]:
        driver.get(url)
        driver.find_element(By.ID, fact).click()
        sect_panel = driver.find_element(By.ID, 'sectoriales')
        sectorial_section = sect_panel.find_element(By.ID, sectorial)
        sectorial_name = sectorial_section.find_element(By.CLASS_NAME, 'nombre_sectorial').text
        driver.find_element(By.ID, sectorial).click()
        collect_army_data(sectorial_name)
#collect_army_data('Japanese Secessionist Army')
"""

driver.quit()