import mysql.connector
import json
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def now_time():
    return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

def load_cookies(driver, cookie_file):
    """加载Cookies到浏览器"""
    try:
        with open(cookie_file, 'r') as cookief:
            cookieslist = json.load(cookief)
            for cookie in cookieslist:
                driver.add_cookie(cookie)
        print("Cookies加载完成")
    except Exception as e:
        print(f"加载Cookies失败: {e}")


def extract_data(sub_driver, url):
    """单独处理子页面数据"""
    try:
        sub_driver.get(url)
        WebDriverWait(sub_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="postdate0"]'))
        )

        publish_time = sub_driver.find_element(By.XPATH, '//*[@id="postdate0"]').text
        publisher_name = sub_driver.find_element(By.XPATH, '//*[@id="postauthor0"]').text
        content_text = sub_driver.find_element(By.XPATH, '//*[@id="postcontent0"]').text

        # 提取 follow_id 和表格统计
        tables = sub_driver.find_elements(By.XPATH, '//*[@id="m_posts_c"]/table')

        print(f"子页面共有 {len(tables)} 个表格")
        
        fellow_ids = []
        elements = sub_driver.find_elements(By.XPATH, '//*[@id="posterinfo6"]/div[1]/span/a')
        numbers = []
        for element in elements:
            element_id = element.get_attribute("id")
            try:
                number = int(element_id.replace("posterinfo", ""))
                numbers.append(number)
            except ValueError:
                pass  # 忽略非数字的 id

        if numbers:
            print(numbers)
        else:
            print("未找到匹配的 posterinfo 元素")

        for index in range(1, len(tables)):
            try:
                follow_id = sub_driver.find_element(By.XPATH, f'//*[@id="postauthor{index}"]').text
                fellow_ids.append(follow_id[4:])
            except Exception as e:
                print(f"提取第 {index + 1} 个表格的 follow_id 失败: {e}")
                fellow_ids.append(None)

        print(f"子页面数据提取成功: {publish_time}, {publisher_name}, 内容长度: {len(content_text)}, 跟帖ID: {fellow_ids}")
    except Exception as e:
        print(f"子页面提取失败: {e}")
        publish_time, publisher_name, content_text, fellow_ids = None, None, None, []

    return publish_time, publisher_name, content_text, fellow_ids


def scrape_data(driver, pages=1, items_per_page=5):
    """抓取主页面内容"""
    collected_data = []
    sub_driver = webdriver.Chrome()  # 子页面浏览器实例
    try:
        for page in range(pages):
            print(f"正在处理第 {page + 1} 页")
            try:
                for item in range(items_per_page):
                    print(f"正在处理第 {item + 1} 条数据")
                    try:
                        row_xpath = f'//*[@id="t_tt{page + 1}_{item}"]'
                        row = driver.find_element(By.XPATH, row_xpath)
                        href = row.get_attribute('href')
                        title = row.text
                        sampling_time = now_time()
                        print(f"采样文章: {title}, 链接: {href}")

                        # 提取子页面数据
                        publish_time, publisher_name, content_text, fellow_ids = extract_data(sub_driver, href)

                        # 构造结果字典
                        collected_data.append({
                            "title": title,
                            "sampling_time": sampling_time,
                            "url": href,
                            "publish_time": publish_time,
                            "publisher_name": publisher_name[4:],  # 去掉"楼主"
                            "content": content_text,
                            "fellow_IDs": fellow_ids,
                        })
                    except Exception as e:
                        print(f"第 {item + 1} 条数据处理失败: {e}")

                # 点击下一页
                next_page_button = driver.find_element(By.XPATH, '//a[@title="加载下一页"]')
                if next_page_button:
                    next_page_button.click()
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, f'//*[@id="t_tt{page + 2}_0"]'))
                    )
                else:
                    print("未找到下一页按钮，结束抓取")
                    break
            except Exception as e:
                print(f"处理第 {page + 1} 页失败: {e}")
    finally:
        sub_driver.quit()
    return collected_data


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
