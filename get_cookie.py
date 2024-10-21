import time
import json
from selenium import webdriver

driver = webdriver.Chrome()

driver.get("https://bbs.nga.cn/thread.php?fid=-7")

time.sleep(40)

with open('cookies.json', 'w', encoding='utf-8') as cookiefile:
    # 将cookies保存为json格式，并格式化输出
    json.dump(driver.get_cookies(), cookiefile, ensure_ascii=False, indent=4)

time.sleep(1)
driver.quit()
