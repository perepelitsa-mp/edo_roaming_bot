import logging
import os
import time
import json
import traceback
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC

import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

path = os.path.join(os.path.dirname(__file__))
attempts = 0
status = False
error_message = ""
bot_name = f'roaming_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'
# Конфиденциальный путь и имя пользователя скрыты
os.system(rf'start /min <FFMPEG_PATH> -y -rtbufsize 100M -f gdigrab -framerate 30 '
        '-probesize 10M -draw_mouse 1 -i desktop -c:v libx264 -r 30 -preset ultrafast -tune zerolatency -crf 25 '
        fr'-pix_fmt yuv420p <VIDEO_OUTPUT_PATH>/{bot_name}.mp4')

file_log = logging.FileHandler(f'{path}/roaming.log')
console_out = logging.StreamHandler()
logging.basicConfig(handlers=(file_log, console_out), format='%(levelname)-8s[%(asctime)s]%(message)s', level=logging.INFO)

try:
    with open(f'{path}/settings.json', encoding="utf-8") as f:
        data = json.load(f)
except UnicodeDecodeError:
    with open(f'{path}/settings.json', encoding="windows-1251") as f:
        data = json.load(f)

id = data['ID']
inn_org = data['inn_org']
email_dlya_svyza = data['email_dlya_svyza']
inn_contr = data['inn_contr']
name_contr = data['name_contr']
oper = data['oper']



while True:
    attempts += 1
    try:
        logging.info(f"id: {id}, inn_org: {inn_org}, email_org: {email_dlya_svyza}, inn_contr: {inn_contr}, oper: {oper}")
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("start-maximized")
            # Конфиденциальный путь к chromedriver скрыт
            driver = webdriver.Chrome(options=options, executable_path = "<CHROMEDRIVER_PATH>")
            driver.implicitly_wait(3)
            driver.get("https://www.diadoc.ru/roaming")
        except:
            error_message = "Ошибка при входе на сайт Диадока"
            raise logging.info(traceback.format_exc())

        try:
            #Ввод для организации
            driver.find_element(By.ID, "Organization").send_keys(inn_org)
            time.sleep(2)
            driver.find_element(By.ID, "Organization").send_keys(Keys.ENTER)
            driver.find_element(By.ID, "Liame").send_keys(email_dlya_svyza)
            driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        except:
            error_message = "Ошибка при вводе данных для организации"
            raise logging.info(traceback.format_exc())

        try:
            #ВВод для контрагента
            if len(inn_contr) == 12:
                org_field = name_contr
                driver.find_element(By.NAME, "Form.Organization").send_keys(org_field)
                time.sleep(2)
                driver.find_element(By.TAG_NAME, 'body').click()
                driver.find_element(By.NAME, "Form.Inn").send_keys(inn_contr)
                time.sleep(2)
                driver.find_element(By.TAG_NAME, 'body').click()
            else:
                org_field = inn_contr
                driver.find_element(By.NAME, "Form.Organization").send_keys(org_field)
                time.sleep(2)
                driver.find_element(By.NAME, "Form.Organization").send_keys(Keys.ENTER)
                time.sleep(2)
            time.sleep(1)
            driver.find_element(By.NAME, "Form.Operator").click()
            time.sleep(2)
            select_element = driver.find_element(By.NAME, "Form.Operator")
            select = Select(select_element)
            logging.info("oper: " + oper)
            for option in select.options:
                if str(oper) in option.text:
                    option.click()
                    break

            driver.find_element(By.TAG_NAME, 'body').click()
            driver.find_element(By.TAG_NAME, 'body').click()
            time.sleep(3)
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-roaming-submit-contractors=""]'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(1)
            button.click()
        except:
            error_message = "Ошибка при вводе данных для контрагента"
            raise logging.info(traceback.format_exc())
        driver.implicitly_wait(15)
        if driver.find_element(By.XPATH, "//p[contains(text(), 'Заявка отправлена')]"):
            status = True
            logging.info(f"Заявка отправлена")
        else:
            error_message = "После ввода всех данных заявка не была отправлена."
            status = False
        driver.quit()
        break
    except:
        os.system(f"taskkill /f /im chrome.exe")
        time.sleep(2)
        if attempts == 3:
            logging.info(f"Первышен лемит ошибок: {traceback.format_exc()}")
            status = False
            break

logging.info(f"Status: {status}")
logging.info(f"error_message: {error_message}")

if status:
    error_message = ''

if str(inn_org) == str(2725026521):
    url = '<URL_1>'
else:
    url = "<URL_2>"

result_params = {
    "ID": id,
    "result": status,
    "error": error_message
}

auth = ('<LOGIN>', '<PASSWORD>')
os.system('taskkill /im ffmpeg.exe')

try:
    response = requests.post(url, json=result_params, auth=auth)
    logging.info(response)
    # Проверка статуса ответа
    if response.status_code == 200:
        print("Запрос успешно выполнен!")
        print("Ответ:", response.text)
    else:
        print(f"Ошибка выполнения запроса: {response.status_code}")
        print("Детали:", response.text)
        status = False
except requests.exceptions.RequestException as e:
    print("Произошла ошибка при отправке запроса:", e)


if status:
    error = {"status": "error", "message": "Error message"}
    file = json.dumps(error)
    error = open(f"{path}/finish.json", "w")
    error.write(file)
    error.close()
else:
    error = {"status": "error", "message": "Error message"}
    file = json.dumps(error)
    json = open(f"{path}/error.json", "w")
    json.write(file)
    json.close()

time.sleep(10)


