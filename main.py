import time
import json
import pandas as pd
from selenium import webdriver

def now_time():
    return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

def load_cookies(driver, cookie_file):
    with open(cookie_file, 'r') as cookief:
        cookieslist = json.load(cookief)
        for cookie in cookieslist:
            driver.add_cookie(cookie)
    print('cookies加载完成')

def scrape_data(driver, pages):
    content = []
    for i in range(pages):
        print(f'第{i + 1}页')

        for j in range(50):
            print(f'第{j + 1}条')
            row_list = driver.find_elements("xpath", f'//*[@id="t_tt{i + 1}_{j}"]')
            hrefs = [element.get_attribute('href') for element in row_list]
            
            for row, href in zip(row_list, hrefs):
                print(row.text)
                title = row.text
                sampling_time = now_time()

                item = {
                    'title': title,
                    'sampling_time': sampling_time,
                    'url': href,
                }
                print(item)
                content.append(item)

        continue_link = driver.find_elements("xpath", '//a[@title="加载下一页"]')
        if continue_link:  # 检查是否找到了链接
            continue_link[0].click()  # 点击列表中的第一个链接
        driver.refresh()
        
    return content

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('https://bbs.nga.cn/thread.php?fid=-7678526')
    driver.delete_all_cookies()
    
    load_cookies(driver, 'cookies.json')
    driver.refresh()
    time.sleep(1)

    content = scrape_data(driver, 3)

    # 写入字典
    data = pd.DataFrame(content)
    data.to_csv("ngaData_" + str(now_time()) + ".csv", index=False, sep=',')

    time.sleep(5)
    driver.quit()
