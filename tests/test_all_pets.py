import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def web_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver
    driver.quit()

def test_show_my_pets(web_driver):
    time.sleep(3)
    web_driver.find_element(By.ID, 'email').send_keys('GaZaG@mail.ru')
    web_driver.find_element(By.ID, 'pass').send_keys('123456')
    web_driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    WebDriverWait(web_driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, 'h1'))
    )
    assert web_driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    images = web_driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = web_driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = web_driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
        WebDriverWait(web_driver, 5).until(
            EC.visibility_of(images[i])
        )
        image_source = images[i].get_attribute('src')
        name_text = names[i].text
        print(f"Image source: {image_source}")
        print(f"Name text: {name_text}")
        assert image_source != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0
