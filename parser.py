import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import urls
from processing import get_button, markup_other_info

months_num = {"янв" : 1,
              "фев" : 2,
              "мар" : 3,
              "апр" : 4,
              "май" : 5,
              "июн" : 6,
              "июл" : 7,
              "авг" : 8,
              "сен" : 9,
              "окт" : 10,
              "ноя" : 11,
              "дек" : 12,
              }


def prepare_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = Service(executable_path="C://Users//keren//Documents//ChromeDriver//chromedriver.exe")
    driver = webdriver.Chrome(service=driver, options=options)
    driver.maximize_window()
    return driver

def check_date_in_days_list(driver, schedule_days, date):
    for iter_day in schedule_days:
        date_text = iter_day.find_element(By.CLASS_NAME, 'schedule__date').text
        day_num, month_num = int(date_text[:6].split()[0]), int(months_num[date_text[:6].split()[1]])
        cur_date = datetime(datetime.now().year, month_num, day_num, 0, 0, 0)
        if cur_date.year == date.year and cur_date.month == date.month and cur_date.day == date.day:
            return True
    return False


def get_schedule(flag, date, group_number):

    driver = prepare_driver()

    group_number = group_number.strip()
    quazitag = group_number[:3]
    parser_status = False
    driver.get(url = urls[quazitag])
    time.sleep(5)

    if flag == "Later":
        schedule_days = driver.find_elements(By.CLASS_NAME, 'schedule__day')
        while not check_date_in_days_list(driver, schedule_days, date):
            buttons = driver.find_elements(By.CLASS_NAME, 'switcher__link')
            for button in buttons:
                button_text = button.text
                if "Следующая неделя" in button_text:
                    button.click()
                    time.sleep(2)
                    break
        schedule_days = driver.find_elements(By.CLASS_NAME, 'schedule__day')
        for day in schedule_days:
            date_text = f"<b>{day.find_element(By.CLASS_NAME, 'schedule__date').text}"
            day_num, month_num = int(date_text[:6].split()[0]), int(months_num[date_text[:6].split()[1]])
            if day_num == date.day and month_num == date.month:
                schedule_text = f"<b>{day.find_element(By.CLASS_NAME, 'schedule__date').text}:</b>\n\n"
                lessons = day.find_elements(By.CLASS_NAME, 'lesson')
                for lesson in lessons:
                    lesson_subject = lesson.find_elements(By.XPATH, '*')
                    time_and_name = lesson_subject[0].text.strip().replace('-', ' — ')
                    other_info = markup_other_info(lesson_subject[1].text.strip())
                    lesson_text = f"<b>{time_and_name}</b>\n"
                    schedule_text += lesson_text
                    schedule_text += other_info
                return schedule_text


    elif flag == "Earlier":
        schedule_days = driver.find_elements(By.CLASS_NAME, 'schedule__day')
        while not check_date_in_days_list(driver, schedule_days, date):
            buttons = driver.find_elements(By.CLASS_NAME, 'switcher__link')
            for button in buttons:
                button_text = button.text
                if "Предыдущая неделя" in button_text:
                    button.click()
                    time.sleep(2)
                    break
        schedule_days = driver.find_elements(By.CLASS_NAME, 'schedule__day')
        for day in schedule_days:
            date_text = f"<b>{day.find_element(By.CLASS_NAME, 'schedule__date').text}"
            day_num, month_num = int(date_text[:6].split()[0]), int(months_num[date_text[:6].split()[1]])
            if day_num == date.day and month_num == date.month:
                schedule_text = f"<b>{day.find_element(By.CLASS_NAME, 'schedule__date').text}:</b>\n\n"
                lessons = day.find_elements(By.CLASS_NAME, 'lesson')
                for lesson in lessons:
                    lesson_subject = lesson.find_elements(By.XPATH, '*')
                    time_and_name = lesson_subject[0].text.strip().replace('-', ' — ')
                    other_info = markup_other_info(lesson_subject[1].text.strip())
                    lesson_text = f"<b>{time_and_name}</b>\n"
                    schedule_text += lesson_text
                    schedule_text += other_info
                return schedule_text

    elif flag == "Today":
        schedule_days = driver.find_elements(By.CLASS_NAME, 'schedule__day')
        for day in schedule_days:
            date_text = f"<b>{day.find_element(By.CLASS_NAME, 'schedule__date').text}"
            day_num, month_num = int(date_text[:6].split()[0]), int(months_num[date_text[:6].split()[1]])
            if day_num == date.day and month_num == date.month:
                schedule_text = f"<b>{day.find_element(By.CLASS_NAME, 'schedule__date').text}:</b>\n\n"
                lessons = day.find_elements(By.CLASS_NAME, 'lesson')
                for lesson in lessons:
                    lesson_subject = lesson.find_elements(By.XPATH, '*')
                    time_and_name = lesson_subject[0].text.strip().replace('-', ' — ')
                    other_info = markup_other_info(lesson_subject[1].text.strip())
                    lesson_text = f"<b>{time_and_name}</b>\n"
                    schedule_text += lesson_text
                    schedule_text += other_info
                return schedule_text
    return "<i>Внутренняя ошибка!</i>"
