import csv

from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import csv
import time
f = open('d3.csv', mode='a', encoding='UTF-8', newline='')
csv_w = csv.DictWriter(f, fieldnames=['职位名称', '技能', '薪资', '学历要求', '地区'])
csv_w.writeheader()

driver_path = r'/usr/local/bin/chromedriver.exe'
driver = webdriver.Chrome(executable_path=driver_path)
keyword = 'python'
url = f"https://www.zhipin.com/web/geek/job?query={keyword}&city=100010000"

def main():
    page = driver.get(url)
    # nextpage = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[1]/div/div/div/a[10]'))
    # )
    #driver.implicitly_wait(2)
    #time.sleep(1)
    for i in range(5):
        time.sleep(1)
        # lis = driver.find_element(By.XPATH, '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[1]/ul/li')
        lis = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[1]/ul/li'))
            # 注意用elements才能拿到全部li
        )

        for li in lis:
            job_name = li.find_element(By.CSS_SELECTOR, '.job-card-body .job-title span').text
            s_lis = li.find_elements(By.CSS_SELECTOR, '.job-card-footer .tag-list li')
            q_list = li.find_elements(By.CSS_SELECTOR, '.job-info .tag-list li')
            salary = li.find_element(By.CSS_SELECTOR, '.job-info .salary').text
            area = li.find_element(By.CSS_SELECTOR, '.job-area-wrapper span').text
            qualify = q_list[-1].text

            a_list = area.split('·')
            area = a_list[0]
            skills = list()
            for s in s_lis:
                skills.append(s.text)
            print(job_name, skills, salary, qualify, area, sep='|')
            dit = {
                '职位名称': job_name,
                '技能': skills,
                '薪资': salary,
                '学历要求': qualify,
                '地区': area
            }
            csv_w.writerow(dit)#写入文件
        driver.find_element(By.CSS_SELECTOR, '.options-pages .ui-icon-arrow-right').click()

    driver.quit()
if __name__ == "__main__":
    main()
