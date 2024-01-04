from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import telegram
import asyncio
import json
def decrypt(input_string):
    decrypted_string = ""
    for char in input_string:
        decrypted_string += chr(ord(char) - 10)
    return decrypted_string
with open('Encrypted.json', 'r') as f:
    Encrypted = json.load(f)
UserToken = Encrypted['Password']
passToken = Encrypted['Email']
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=chrome_options)
bot_token = Encrypted['API']
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
driver.get(login_url)
async def wait_for_element():
    parent_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='col-xl-10']")))
    element = WebDriverWait(parent_div, 10).until(EC.presence_of_all_elements_located((By.XPATH, ".//div[@class='container-fluid mt-2']")))
    return element
text_found= False
async def check_divs(texts_to_check,found):
    text_to_send=[]
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
        await asyncio.sleep(10)
async def refreshData():
    apply_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='mobileLeftMenu_li_link' and text()='APPLY']")))
    apply_link.click()
async def printData():
    while True:
        try:
            await check_divs(texts_to_check,text_found)
        except Exception as e:
            print("An error occurred:", e)
            break  # Break the loop in case of any exception/error
wait = WebDriverWait(driver, 86400)
language_option_button = WebDriverWait(driver, 86400).until(EC.presence_of_element_located((By.XPATH, "//button[@id='rfs-btn']")))
language_option_button.click()
language_option = WebDriverWait(driver, 86400).until(EC.presence_of_element_located((By.XPATH, "//li[@id='rfs-GB']")))
language_option.click()
username_input = wait.until(EC.presence_of_element_located((By.NAME, username_field_name)))
password_input = driver.find_element(By.NAME, password_field_name)
username_input.send_keys(token2)
password_input.send_keys(token1)
login_button = driver.find_element(By.XPATH, "//button[contains(@class, 'btn_next') and contains(span, 'Next')]")
login_button.click()











































async def main():
    try:
        redirected_url = wait.until(EC.url_to_be("https://portal.edu.az/services"))

        if redirected_url:
            print("Login successful. Redirected to:", redirected_url)
            service_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'servicesMobile_body_nav--li') and contains(text(), 'SERVICES')]")))
            service_option.click()
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='surTdFLx' and text()='Apply to higher and secondary special education institutions']")))
            element.click()
            await printData()

        else:
            print("Login successful but not redirected to the expected URL.")
    except TimeoutException:
        print("Login failed or not redirected.")
if __name__ == "__main__":
    asyncio.run(main())
