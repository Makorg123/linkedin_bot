import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
import time

load_dotenv()

def get_credentials():
    username = os.getenv("LINKEDIN_USERNAME")
    password = os.getenv("LINKEDIN_PASSWORD")
    print(f"Username: {username}, Password: {password}")  
    return username, password

def setup_driver(driver_path):
    service = Service(driver_path)
    return webdriver.Edge(service=service)

def login_to_linkedin(driver, username, password):
    driver.get("https://www.linkedin.com/login")
    print("Navigated to LinkedIn login page") 
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    print("Logged in to LinkedIn")  

def search_for_job(driver, job_title):
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']")))
    search_box.send_keys(job_title)
    search_box.send_keys(Keys.RETURN)
    print(f"Searched for job: {job_title}") 

def filter_people(driver):
    people_filter = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='People']")))
    people_filter.click()
    print("Filtered search results to people")  

def send_connection_request(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    connect_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Connect')]")
    print(f"Found {len(connect_buttons)} 'Connect' buttons.")  
    if connect_buttons:
        button = connect_buttons[0]
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button)).click()
        send_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Send now']")))
        send_button.click()
        print("Connection request sent.")
    else:
        print("No 'Connect' buttons found.")

def main():
    linkedin_username, linkedin_password = get_credentials()
    driver_path = r"C:\\Users\\Hp\Downloads\\edgedriver_win64\\msedgedriver.exe"
    driver = setup_driver(driver_path)
    try:
        login_to_linkedin(driver, linkedin_username, linkedin_password)
        time.sleep(5)
        search_for_job(driver, "Data Scientist OR Lead Data Scientist")
        time.sleep(5)
        filter_people(driver)
        time.sleep(5)
        send_connection_request(driver)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()
        print("Bot finished.")

if __name__ == "__main__":
    main()