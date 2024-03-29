###########################################################################################################################
###################     See https://www.infinitytheacademy.com/basic/reading-profiles/      ###############################
###################                         for infinity explaination                       ###############################
###################                                                                         ###############################
###########################################################################################################################


from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import re
import mysql.connector

mydb = mysql.connector.connect(
    host = '127.0.0.1',
    user = 'army_db',
    password = 'Infinity082791',
    database = 'army_db'
)

mycursor = mydb.cursor()

# Establish chrome driver and go to report site URL
url = "https://infinitytheuniverse.com/army/infinity"
# service = Service(executable_path="C:/Users/Bulmu/Documents/python/Data Science Practice/army_recommender/Infinity-Data_Science_Project")
driver = webdriver.Firefox()
driver.get(url)
driver.implicitly_wait(10)
driver.title
driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/div[2]/div[2]/button[3]').click()
driver.implicitly_wait(0.5)


def faction_sectorial_list():
    #### Find and create list of faction ids  #####

    # mycursor.execute('''CREATE TABLE IF NOT EXISTS factions (
    #     army VARCHAR(50),
    #     sectorial VARCHAR(50),
    #     sec_no VARCHAR(50),
    #     PRIMARY KEY (sectorial)
    # )''')
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
        sectorial_df = pd.DataFrame.from_dict(faction_sectorial_dict, orient='index', columns=['Sectorial ID', 'Sectorial Name'])
        sectorial_df.to_csv(f'sectorial_dataframe')
    
    #####  Add factions and sectorials to sql db  ########
    # for item in faction_sectorial_dict.values():
    #     sql = 'INSERT INTO factions (army, sectorial, sec_no) VALUES (%s, %s, %s)'
    #     if item[1][0] == 'Druze Bayram Security':
    #         army = 'NA2'
    #     else:
    #         army = item[1][0]
    #     print(army)
    #     for i in range(len(item[0])):
    #         val = (army, item[1][i], item[0][i])
    #         mycursor.execute(sql,val)
    # mydb.commit()

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

    mycursor.execute('''CREATE TABLE IF NOT EXISTS units (
        unit_name VARCHAR(100) NOT NULL,
        sec_no VARCHAR(50),
        unit_type VARCHAR(5),
        classification VARCHAR(100),
        mov_1 INT,
        mov_2 INT,
        cc INT,
        bs INT,
        ph INT,
        wip INT,
        arm INT,
        bts INT,
        w INT,
        s INT,
        ava INT,
        equipment_1 VARCHAR(50),
        equipment_2 VARCHAR(50),
        equipment_3 VARCHAR(50),
        equipment_4 VARCHAR(50),
        equipment_5 VARCHAR(50),
        equipment_6 VARCHAR(50),
        equipment_7 VARCHAR(50),
        skills_1 VARCHAR(50),
        skills_2 VARCHAR(50),
        skills_3 VARCHAR(50),
        skills_4 VARCHAR(50),
        skills_5 VARCHAR(50),
        skills_6 VARCHAR(50),
        skills_7 VARCHAR(50),
        skills_8 VARCHAR(50),
        skills_9 VARCHAR(50),
        skills_10 VARCHAR(50),
        skills_11 VARCHAR(50),
        skills_12 VARCHAR(50),
        skills_13 VARCHAR(50),
        skills_14 VARCHAR(50),
        skills_15 VARCHAR(50),
        regular BINARY,
        irregular BINARY,
        impetuous BINARY,
        unit_cube BINARY,
        hackable BINARY,
        CONSTRAINT unit_key PRIMARY KEY (unit_name, sec_no)
    )''')

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
        movement = value[1][0].split('-')
        unit_mov.append(value[1][0])
        unit_cc.append(value[1][1])
        unit_bs.append(value[1][2])
        unit_ph.append(value[1][3])
        unit_wip.append(value[1][4])
        unit_arm.append(value[1][5])
        unit_bts.append(value[1][6])
        unit_w.append(value[1][7])
        unit_s.append(value[1][8])
        if isinstance(value[1][9], int):
            unit_ava.append(value[1][9])
        elif value[1][9] == "Total":
            unit_ava.append(20)
        else:
            unit_ava.append(0)
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

    print(len(unit_name))
    print(len(sectorial_list))
    print(len(unit_type))
    print(len(unit_classification))
    print(len(unit_mov))
    print(len(unit_cc))
    print(len(unit_bs))
    print(len(unit_ph))
    print(len(unit_wip))
    print(len(unit_arm))
    print(len(unit_bts))
    print(len(unit_w))
    print(len(unit_s))
    print(len(unit_ava))
    #### Insert all info into sql db for base units
    print(unit_name)
    for i in range(len(unit_name)):
        sql = 'INSERT INTO units (unit_name, sec_no, unit_type, classification, mov_1, mov_2, cc, bs, ph, wip, arm, bts, w, s, ava) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        val = (unit_name[i], sectorial_list[i], unit_type[i], unit_classification[i], unit_mov[i][0], unit_mov[i][2], unit_cc[i], unit_bs[i], unit_ph[i], unit_wip[i], unit_arm[i], unit_bts[i], unit_w[i], unit_s[i], unit_ava[i])
        mycursor.execute(sql,val)
        mydb.commit()

    army_df = pd.DataFrame(list(zip(unit_name, sectorial_list, unit_type, unit_classification, unit_mov, unit_cc, unit_bs, unit_ph, unit_wip, unit_arm, unit_bts, unit_w, unit_s, unit_ava, unit_equip, unit_special, unit_characteristics_list)), columns = ['Name', 'Sectorial', 'Type', 'Classification', 'MOV', 'CC', 'BS', 'PH', 'WIP', 'ARM', 'BTS', 'W', 'S', 'AVA', 'Equipment', 'Special Skills', 'Characteristics'])
    print(army_df)
    sub_df = pd.DataFrame.from_dict(sub_units, orient='index', columns=['Weapon(s)', 'Melee Weapons', 'SWC', 'C', 'Base Name'])
    sub_df.to_csv(f'{sect_name}_sub-units_dataframe')
    army_df.to_csv(f'{sect_name}_dataframe')

    return 


def collect_weapon_data():
    driver.get(url)
    driver.find_element(By.ID, 'fac_101').click()
    principal_panel = driver.find_element(By.ID, "Principal")
    principal_panel.find_element(By.ID, 'icon_lista_armas').click()
    weap_panel = driver.find_element(By.ID, 'contenedor_lineas_armas')
    weapons_html_list = weap_panel.find_elements(By.CSS_SELECTOR, '.linea_arma.clearfix.ng-star-inserted')
    weapons_dict = {}
    weap_list = []
    for weap in weapons_html_list:
        driver.implicitly_wait(0.5)
        weap_name = weap.find_element(By.CLASS_NAME, 'arma_nombre').text
        weap_list.append(weap_name)
        #print(weap_name)
    # print(weap_list)
    distances = weap.find_elements(By.CSS_SELECTOR, '.distancias.ng-star-inserted')
    for i in range(len(weap_list)):
        #print(f'Weapon: {weap_list[i]}')
        weapons_dict[weap_list[i]] = [[],[],[],[],[],[]]
        for dist in distances:
            #modifiers = []
            for j in range(4):
                try:
                    width = dist.find_element(By.XPATH, f'//*[@id="contenedor_lineas_armas"]/div[{i+1}]/div[2]/div[{j+1}]').get_attribute('style')  # width: 30px;
                    width_num = re.findall(r'(\d+)', width)
                    # print(f'Width: {int(width_num[0])}')
                    modifier = dist.find_element(By.XPATH, f'//*[@id="contenedor_lineas_armas"]/div[{i+1}]/div[2]/div[{j+1}]').text # append this * width/30
                    # print(f'Modifier: {modifier}')
                    weapons_dict[weap_list[i]][0].extend([modifier]*int(int(width_num[0])/30))
                except:
                    pass
        #outside of distances
        weapons_dict[weap_list[i]][1].append(weap.find_element(By.XPATH, f'//*[@id="contenedor_lineas_armas"]/div[{i+1}]/div[3]').text)
        weapons_dict[weap_list[i]][2].append(weap.find_element(By.XPATH, f'//*[@id="contenedor_lineas_armas"]/div[{i+1}]/div[4]').text)
        weapons_dict[weap_list[i]][3].append(weap.find_element(By.XPATH, f'//*[@id="contenedor_lineas_armas"]/div[{i+1}]/div[5]').text)
        weapons_dict[weap_list[i]][4].append(weap.find_element(By.XPATH, f'//*[@id="contenedor_lineas_armas"]/div[{i+1}]/div[6]').text)
        weapons_dict[weap_list[i]][5].append(weap.find_element(By.XPATH, f'//*[@id="contenedor_lineas_armas"]/div[{i+1}]/div[7]').text)

        print(i)
    mycursor.execute('''CREATE TABLE IF NOT EXISTS weapons (
            weapon_name VARCHAR(50),
            band_8 INT,
            band_16 INT,
            band_24 INT,
            band_32 INT,
            band_40 INT,
            band_48 INT,
            band_72 INT,
            band_96 INT,
            damage_stat VARCHAR(5),
            damage_int INT,
            burst INT,
            ammo VARCHAR(15),
            saving_roll VARCHAR(10),
            trait_1 VARCHAR(50),
            trait_2 VARCHAR(50),
            trait_3 VARCHAR(50),
            trait_4 VARCHAR(50),
            trait_5 VARCHAR(50),
            trait_6 VARCHAR(50),
            trait_7 VARCHAR(50),
            trait_8 VARCHAR(50),
            trait_9 VARCHAR(50),
            trait_10 VARCHAR(50),
            PRIMARY KEY (weapon_name)
        )''')

    sql = 'INSERT INTO weapons (weapon_name, band_8, band_16, band_24, band_32, band_40, band_48, band_72, band_96, damage_stat, damage_int, burst, ammo, saving_roll) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    for key in weapons_dict.keys():
        # print(f'Name: {key}')
        if 1 <= len(weapons_dict[key][0]):
            range1 = int(weapons_dict[key][0][0])
            # print(f'Range band 0-8: {int(weapons_dict[key][0][0])}')
        else:
            range1 = None
        if 2 <= len(weapons_dict[key][0]):
            range2 = int(weapons_dict[key][0][1])
            # print(f'Range band 8-16: {int(weapons_dict[key][0][1])}')
        else:
            range2 = None
        if 3 <= len(weapons_dict[key][0]):
            range3 = int(weapons_dict[key][0][2])
            # print(f'Range band 16-24: {int(weapons_dict[key][0][2])}')
        else:
            range3 = None
        if 4 <= len(weapons_dict[key][0]):
            range4 = int(weapons_dict[key][0][3])
            # print(f'Range band 24-32: {int(weapons_dict[key][0][3])}')
        else:
            range4 = None
        if 5 <= len(weapons_dict[key][0]):
            range5 = int(weapons_dict[key][0][4])
            # print(f'Range band 32-40: {int(weapons_dict[key][0][4])}')
        else:
            range5 = None
        if 6 <= len(weapons_dict[key][0]):
            range6 = int(weapons_dict[key][0][5])
            # print(f'Range band 40-48: {int(weapons_dict[key][0][5])}')
        else:
            range6 = None
        if 7 <= len(weapons_dict[key][0]):
            range7 = int(weapons_dict[key][0][6])
            # print(f'Range band 48-72: {int(weapons_dict[key][0][6])}')
        else:
            range7 = None
        if 8 <= len(weapons_dict[key][0]):
            range8 = int(weapons_dict[key][0][7])
            # print(f'Range band 72-96: {int(weapons_dict[key][0][7])}')
        else:
            range8 = None
        if weapons_dict[key][1][0] == 'PH' or weapons_dict[key][1][0] == 'WIP' or weapons_dict[key][1][0] == '-' or weapons_dict[key][1][0] == '*':
            dam_stat = weapons_dict[key][1][0]
            dam_int = None
            # print(f'Damage stat: {weapons_dict[key][1][0]}')
        else:
            dam_stat = None
            dam_int = weapons_dict[key][1][0]
            # print(f'Damage int: {weapons_dict[key][1][0]}')
        if isinstance(weapons_dict[key][2][0], int) == True:
            burst = int(weapons_dict[key][2][0])
        else:
            burst = None
        # print(f'Burst: {int(weapons_dict[key][2][0])}')
        ammo = weapons_dict[key][3][0]
        # print(f'Ammo: {weapons_dict[key][3][0]}')
        saving = weapons_dict[key][4][0]
        # print(f'Saving Roll: {weapons_dict[key][4][0]}')
        val = (key, range1, range2, range3, range4, range5, range6, range7,range8, dam_stat, dam_int, burst, ammo, saving)
        mycursor.execute(sql,val)
        mydb.commit()

        traits_sql = 'UPDATE weapons SET trait_%s = %s WHERE weapon_name = %s'

        trait_list = weapons_dict[key][5][0].split(' - ')
        
        for i in range(len(trait_list)):
            # print(f'Trait{i+1}: {trait_list[i]}')
            traits_val = (i+1, trait_list[i], key)
            # print(traits_val)
            mycursor.execute(traits_sql,traits_val)
            mydb.commit()
    
    # driver.get(url)
    # driver.find_element(By.ID, 'fac_101').click()  #opens menu
    # principal_panel = driver.find_element(By.ID, "Principal")
    # principal_panel.find_element(By.ID, 'icon_lista_armas').click()  #opens weapon panel
    # weap_panel = driver.find_element(By.ID, 'contenedor_lineas_armas')
    # weapons_html_list = weap_panel.find_elements(By.CSS_SELECTOR, '.linea_arma.clearfix.ng-star-inserted')
    # weapons_dict = {}
    # weap_list = []
    # for weap in weapons_html_list:
    #     driver.implicitly_wait(0.5)
    #     weap_name = weap.find_element(By.CLASS_NAME, 'arma_nombre').text
    #     weap_list.append(weap_name)
    # distances = weap.find_elements(By.CSS_SELECTOR, '.distancias.ng-star-inserted')
    # for i in range(len(weap_list)):
    #     weapons_dict[weap_list[i]] = [[],[],[],[],[],[]]
    #     for dist in distances:
    #         for j in range(4):
    #             try:
    #                 width = dist.find_element(By.XPATH, f'//*[@id="contenedor_lineas_armas"]/div[{i+1}]/div[2]/div[{j+1}]').get_attribute('style')  # width: 30px;
    #                 width_num = re.findall(r'(\d+)', width)
    #                 modifier = dist.find_element(By.XPATH, f'//*[@id="contenedor_lineas_armas"]/div[{i+1}]/div[2]/div[{j+1}]').text # append this * width/30
    #                 weapons_dict[weap_list[i]][0].extend([modifier]*int(int(width_num[0])/30))
    #             except:
    #                 pass
    #     weapons_dict[weap_list[i]][1].append(weap.find_element(By.XPATH, f'//*[@id="contenedor_lineas_armas"]/div[{i+1}]/div[3]').text)
    #     weapons_dict[weap_list[i]][2].append(weap.find_element(By.XPATH, f'//*[@id="contenedor_lineas_armas"]/div[{i+1}]/div[4]').text)
    #     weapons_dict[weap_list[i]][3].append(weap.find_element(By.XPATH, f'//*[@id="contenedor_lineas_armas"]/div[{i+1}]/div[5]').text)
    #     weapons_dict[weap_list[i]][4].append(weap.find_element(By.XPATH, f'//*[@id="contenedor_lineas_armas"]/div[{i+1}]/div[6]').text)
    #     weapons_dict[weap_list[i]][5].append(weap.find_element(By.XPATH, f'//*[@id="contenedor_lineas_armas"]/div[{i+1}]/div[7]').text)
    # weapon_df = pd.DataFrame.from_dict(weapons_dict, orient='index', columns=['Range Modifiers', 'Damage', 'Burst', 'Ammo', 'Saving Roll', 'Traits'])
    # weapon_df.to_csv(f'weapons_dataframe')    
    # return



faction_sectorial_dict = faction_sectorial_list()  #runs function to find all sectorials.  Used to run collect army data function


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


driver.quit()