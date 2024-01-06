from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import telegram
import asyncio
import json
import os

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 5)

DBpath = '../MYPORTALMONITORER/Credentials/Encrypted.json'
def load_from_json(path): return json.load(open(path, 'r'))

Encrypted = load_from_json(DBpath)
UserToken = Encrypted['Password']
passToken = Encrypted['Email']
bot_token = Encrypted['API']

cookies = '../MYPORTALMONITORER/auth/cookies.json'
Local_Storage = '../MYPORTALMONITORER/auth/local_storage.json'

async def save_to_json(data, path): os.makedirs(os.path.dirname(path), exist_ok=True); json.dump(data, open(path, 'w'))

async def add_cookies(cookies): [driver.add_cookie(cookie) for cookie in cookies]
async def add_local_storage(local_storage): [driver.execute_script(f"window.localStorage.setItem('{k}', '{v}');") for k, v in local_storage.items()]

async def Get_Directory(path): return os.path.normpath(path).split(os.sep)[2]

def decrypt(input_string):
    decrypted_string = ""
    for char in input_string:
        decrypted_string += chr(ord(char) - 10)
    return decrypted_string

bot = telegram.Bot(token=bot_token)
chat_id=Encrypted['CID']


async def sendupdate(textt):
    await bot.send_message(decrypt(chat_id), text=textt)

login_url = 'https://portal.edu.az/'
username_field_name = 'email'
password_field_name = 'password'
texts_to_check = ['''submitted''','''expired''']
token2=decrypt(passToken)
token1=decrypt(UserToken)


async def wait_for_element():
    parent_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='col-xl-10']")))
    element = WebDriverWait(parent_div, 10).until(EC.presence_of_all_elements_located((By.XPATH, ".//div[@class='container-fluid mt-2']")))
    return element


async def check_divs(texts_to_check):
    text_to_send=[]
    found = False
    await refreshData()
    divs = await wait_for_element()
    for div in divs:
        for text in texts_to_check:
            if text in div.text:
                found = True
        if not found:
            text_to_send.append(div.text)
    await refreshData()
    for string in text_to_send:
        await sendupdate(string)
        await asyncio.sleep(60)


async def refreshData():
    apply_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='mobileLeftMenu_li_link' and text()='APPLY']")))
    apply_link.click()


async def printData():
    while True:
        try:
            await check_divs(texts_to_check)
        except Exception as e:
            print("An error occurred:", e)
            break

async def login():
    driver.get(login_url)
    language_option_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='rfs-btn']")))
    language_option_button.click()
    language_option = wait.until(EC.presence_of_element_located((By.XPATH, "//li[@id='rfs-GB']")))
    language_option.click()
    await asyncio.sleep(1)
    if os.path.exists(cookies) and os.path.exists(Local_Storage):
        await add_cookies(load_from_json(cookies))
        await add_local_storage(load_from_json(Local_Storage))
        if await skip_if_Cookie_Works():
            return
        else:
            await delete_folder(await Get_Directory(cookies))
    username_input = wait.until(EC.presence_of_element_located((By.NAME, username_field_name)))
    password_input = driver.find_element(By.NAME, password_field_name)
    username_input.send_keys(token2)
    password_input.send_keys(token1)
    login_button = driver.find_element(By.XPATH, "//button[contains(@class, 'btn_next') and contains(span, 'Next')]")
    login_button.click()
    await asyncio.sleep(3)
    await save_to_json(driver.get_cookies(), cookies)
    await save_to_json({key: driver.execute_script(f"return window.localStorage.getItem('{key}');") for key in driver.execute_script("return Object.keys(window.localStorage);")}, Local_Storage)

async def delete_folder(folder_path):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            await delete_folder(file_path) if os.path.isdir(file_path) else os.remove(file_path)
        os.rmdir(folder_path)

async def login_check():
    try:
        wait.until(EC.url_to_be("https://portal.edu.az/services"))
        return True
    except:
        return False


async def skip_if_Cookie_Works():
    if await login_check():
        await save_to_json(driver.get_cookies(), cookies)
        await save_to_json({key: driver.execute_script(f"return window.localStorage.getItem('{key}');") for key in driver.execute_script("return Object.keys(window.localStorage);")}, Local_Storage)
        return True
    else:
        return False


async def main():
    await login()
    try:
        redirected_url = wait.until(EC.url_to_be("https://portal.edu.az/services"))

        if redirected_url:
            print("Login successful. Redirected to:", redirected_url)
            service_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'servicesMobile_body_nav--li') and contains(text(), 'SERVICES')]")))
            service_option.click()
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='surTdFLx' and text()='Apply to higher and secondary special education institutions']")))
            element.click()
            await printData()
            driver.close()
            driver.quit()
        else:
            print("Login successful but not redirected to the expected URL.")
    except TimeoutException:
        print("Login failed or not redirected.")
if __name__ == "__main__":
    asyncio.run(main())
