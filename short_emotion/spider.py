import json
import logging
import requests
import os
from selenium.webdriver.edge.service import Service as EdgeService
from selenium import webdriver
from utils.browser_utils import get_browser_driver
from pathlib import Path

logger = logging.getLogger(__name__)

def get_stock_data():
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0'

        cookie = 'Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1739026419; Hm_lvt_722143063e4892925903024537075d0d=1739026509; Hm_lvt_929f8b362150b1f77b477230541dbbc2=1739026509;'
        url = 'https://q.10jqka.com.cn/api.php?t=indexflash'
        headers = {
            'User-Agent': user_agent,
            'cookie': cookie,
            'Referer': 'https://q.10jqka.com.cn/'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_data = json.loads(response.text)
        up_count = json_data["zdfb_data"]["znum"]
        down_count = json_data["zdfb_data"]["dnum"]
        up_floor_count = json_data["zdt_data"]["last_zdt"]["ztzs"]
        down_floor_count = json_data["zdt_data"]["last_zdt"]["dtzs"]
        print(f"up_count: {up_count}, down_count: {down_count}, up_floor_count: {up_floor_count}, down_floor_count: {down_floor_count}")
    except requests.RequestException as e:
        logger.error(f"大盘基本涨跌信息获取请求出错: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"大盘基本涨跌信息获取解析出错: {str(e)} ")
        raise e

def get_short_emotion():
    try:
        driver = get_browser_driver()
        driver.get('https://q.10jqka.com.cn/')
        driver.implicitly_wait(3)
        print(driver.title)
        print(driver.page_source)
        driver.quit()


        # print(f"up_count: {up_count}, down_count: {down_count}, up_floor_count: {up_floor_count}, down_floor_count: {down_floor_count}")
    except requests.RequestException as e:
        logger.error(f"大盘基本涨跌信息获取请求出错: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"大盘基本涨跌信息获取解析出错: {str(e)} ")
        raise e