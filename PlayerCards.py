import time
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import sys

if len(sys.argv) != 3:
    exit(1)
options = EdgeOptions()
# 禁用可视化
options.add_argument('--headless') 
options.use_chromium = True
# 浏览器的位置
# options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" 
options.add_argument('window-size=1796x749')
driver = Edge(options=options)
try:
    driver.get("https://enka.shinshin.moe/u/" + sys.argv[1])
    if driver.get_cookie("locale")["value"] != "zh-CN":
        driver.delete_all_cookies()
        driver.add_cookie({"name" : "locale", "value" : "zh-CN"})
        driver.get("https://enka.shinshin.moe/u/" + sys.argv[1])
    for i in range(1,len(driver.find_elements(by=By.XPATH,value="/html/body/main/content/div[2]/div"))+1):
        if driver.find_element(by=By.XPATH, value="/html/body/main/content/div[2]/div[" + str(i) + "]").get_attribute("class") == "flex-break svelte-188i0pk":
            continue
        driver.find_element(by=By.XPATH, value="/html/body/main/content/div[2]/div[" + str(i) + "]").click()
        CharacterName = driver.find_element(by=By.XPATH, value="/html/body/main/content/div[3]/div[2]/div/div/div[2]/div[2]").text
        if CharacterName == sys.argv[2]:
            time.sleep(8)
            driver.find_element(by=By.XPATH,value="/html/body/main/content/div[3]/div[1]/button").click()
            img = WebDriverWait(driver, 10, 0.5).until(
                      EC.presence_of_element_located((By.XPATH, "/html/body/main/content/div[3]/img"))
                      )
            img_link = img.get_attribute("src")
            driver.execute_script(f'window.open("{img_link}", "_blank");')
            driver.switch_to.window(driver.window_handles[-1])
            driver.save_screenshot(sys.argv[1]+sys.argv[2]+".png")
            break
    driver.close() 
except Exception as e:
    print(e)
    driver.close()