from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep, ctime
import numpy as np
import json

options = webdriver.FirefoxOptions()
options.set_preference("dom.webriver.enabled", False)
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Firefox(options=options)
driver.implicitly_wait(10)
driver.get("https://www.tyuiu.ru/incoming/")

def get_table():
    print(f'Getting the table...')
    org = driver.find_element_by_name('org')

    org_all_options = org.find_elements_by_tag_name("option")
    for option in org_all_options:
        if option.get_attribute("value") == '8':
            option.click()

    eduform = driver.find_element_by_name('eduform')

    eduform_all_options = eduform.find_elements_by_tag_name("option")
    for option in eduform_all_options:   
        if option.get_attribute("value") == '1':  
            option.click()

    direction = driver.find_element_by_name('direction')

    direction_all_options = direction.find_elements_by_tag_name("option")
    for option in direction_all_options:    
       if option.get_attribute("value") == '2':
            option.click()

    prof = driver.find_element_by_name('prof')
    prof_all_options = prof.find_elements_by_tag_name("option")
    for option in prof_all_options:
       if option.get_attribute("value") == '09.02.01 Компьютерные системы и комплексы (на базе 9 кл.)':
            option.click()

    btn_success = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/div/form[1]/button')

    btn_success.click()
    table = driver.find_element_by_css_selector('#table > tbody:nth-child(1)')
    
    print('OK! The table has gotten!')
    return table

def table_to_dict(table):
    print('Getting the users from table')
    fields = table.find_elements_by_css_selector("tr:not(tr:nth-child(1))")
    users = {}
    j = 0
    for field in fields:
        data_field = field.find_elements_by_tag_name("td")
        users[str(j)] = {
             'number': data_field[0].text,
             'name': data_field[1].text,
             'score': data_field[2].text.replace(',', '.'),
             'type': data_field[3].text,
             'original': data_field[4].text
        }
        j+=1
    driver.close()
    print('OK! Users have gotten!')
    return users

def average_of_score(users, use_my_score=False):
    print('Counting the average of scores...')
    scores = []
    for user in users.values():
        scores.append(float(user['score']))
    total_score = np.sum(scores)
    count_of_scores = len(scores)
    print('OK! The average of scores has gotten')
    if use_my_score:
        with open('./table_of_marks.json', 'r') as my_marks:
            data = json.load(my_marks)
            my_score = data['average']
        scores.append(my_score)
        total_score = np.sum(scores)
        count_of_scores+=1
    return total_score/count_of_scores

def tofile(users):
    print('Saving the data to file')
    with open(f'./students\' list from {ctime()}.txt','w') as file:
        data = ''
        data += f'Всего учеников: {len(users.values())}\n'
        data += f'Средний балл аттетстата всех учеников: {average_of_score(users)}\n'
        data += f'Если учитывать твой средние балл: 4.263\n'
        data += f'То получается: {average_of_score(users, True)}\n'
        nl = f'\n------------------------------\n\n'
        for user in users.values():
            data += nl
            data += f'Номер: {user["number"]}\n'
            data += f'Ф.И.О: {user["name"]}\n'
            data += f'Средний балл аттестата: {user["score"]}\n'
            data += f'Вид приёма: {user["type"]}\n'
            data += f'Оригиналы: {user["original"]}\n'
            if (user["name"] == 'Васильев Александр Алексеевич' or user["name"] == 'Летунов Кирилл Викторович'):
                print(f'Имя: {user["name"]}\nНомер: {user["number"]}\nСредний балл аттестата: {user["score"]}\n')
        data += nl
        file.write(data)
    print('OK! The data has saved to file!')


if __name__=="__main__":
   print('Starting work...\n')
   table =  get_table()
   users = table_to_dict(table)
   tofile(users)
   print('\nOK! All has done!')
