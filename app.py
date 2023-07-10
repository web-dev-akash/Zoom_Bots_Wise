from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from multiprocessing import Process
from selenium.webdriver.support.wait import WebDriverWait
import random
from flask import Flask
import os
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service
service = Service(executable_path="./chromedriver/chromedriver")

load_dotenv()

meet_code = os.getenv('MEET_ID')
passcode = os.getenv('PASSCODE')


app = Flask(__name__)


def join(meet, password, name):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    choice = [0, 1, 2]
    driver.get(f'https://zoom.us/wc/join/{meet}')

    WebDriverWait(driver, timeout=300).until(lambda d: d.find_element(By.ID, "input-for-pwd"))  # to let the webpage open completely

    driver.find_element(By.ID, "input-for-pwd").send_keys(password)

    # driver.find_element("//a[@id='btnSubmit']").click()
    driver.find_element(By.ID, "input-for-name").send_keys(name)

    time.sleep(2)

    driver.find_element(By.CLASS_NAME, "preview-join-button").click()

    WebDriverWait(driver, timeout=300).until(lambda d: d.find_element(By.CLASS_NAME, "join-audio-by-voip__join-btn"))

    driver.find_element(By.CLASS_NAME, "join-audio-by-voip__join-btn").click()

    time.sleep(10)

    driver.find_element(By.CLASS_NAME, "more-button").click()

    WebDriverWait(driver, timeout=900).until(lambda d: d.find_element(By.XPATH, "//a[@aria-label='Breakout Rooms']"))

    driver.find_element(By.XPATH, "//a[@aria-label='Breakout Rooms']").click()

    roombtns = driver.find_elements(By.CLASS_NAME, "bo-room-item-container__join-btn")
    option = random.choice(choice)
    roombtns[option].click()
    driver.find_element(By.CLASS_NAME, "confirm-tip__footer-btn").click()

    time.sleep(5400)
    driver.quit()



first_names = ['Aarav', 'Aayush', 'Abhinav', 'Aditi', 'Akash', 'Alisha', 'Aman', 'Amit', 'Anaya', 'Anika','Anirudh', 'Anita', 'Anjali', 'Ansh', 'Arjun', 'Arun', 'Arushi', 'Aryan', 'Avantika', 'Ayush']

#
# join(meet_code, passcode, "Test", 1)


def handle_get_request():
    for num in range(10):
        Process(target=join, args=(meet_code, passcode, first_names[num])).start()


@app.route('/', methods=['GET'])
def index():
    handle_get_request()
    return "Request Successful!"


if __name__ == '__main__':
    app.run()
