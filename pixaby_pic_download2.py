#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/3/11 18:00
# @Author  : CUI liuliu
# @File    : pixaby_pic_download2.py
import logging
import os
import random
import time
# from random import random

import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

import mysql.connector

log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.FileHandler('download_images.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0",
    "cookie": "anonymous_user_id=ccb905077da945e7b5f12786aaa13ff3; is_human=1; lang=zh; dwf_search_ai_tags=True; OptanonAlertBoxClosed=2025-03-18T09:53:24.355Z; csrftoken=kzs51sIlD2CTyw99jgkjKqMvJbVCeyKb; sessionid=.eJxVjkEOgyAQRe_CujGiwDC9DBlxqLSKjcCq6d2rLpp2_d5_-S_hqJbJ1cybi6O4CoWdla1V4vKLBvIPTgd_buudfWlqiXNufM1lXU6xiaeaaGG3bo4XivN39xebKE97aZB-NGBU0IyKoFeAg9VdT4A9Y4u6A_QYAgNIb4gUsuZRcpAm7B_tEZ0p3SrdeM9xEu8P7A9ELA:1tuj09:ven5WbMZ6fDqE3aUjZl-wrQWkUd2iDPOW7GBt_TEurg; dwf_show_canva_banner_ads=True; client_width=1279; _sp_id.aded=37be0959-0e18-43ae-9c8b-7831c0c2f848.1741684292.9.1742801933.1742450365.3a4173fb-425d-4bcb-8860-06cc70b4131c.fcccc68f-b0fd-406d-badb-0ea9e699c1e2.fb5ca0bf-0eb6-40c8-b093-3eaae5d04aa7.1742801933452.1; user_id=49281084; __cf_bm=LsmnGzCBfklx3SuTCJIlOMKHeb2IslXsti4PgjtiJqg-1743145984-1.0.1.1-e_Fd5bCZ7PW30L4mcOC6xiIU1ecMdWFq0aax0zqtd7l2f5KheyQKLcfSaubFUUX2HlnB0voIs31HBn_bMa7XL44FY2ywrDSTpJ4cyVhMFgo; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Mar+28+2025+15%3A13%3A05+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202401.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=e8ff9e60-e11e-4472-a04a-91fefa74d4db&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=JP%3B13",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}


def download_image(url, save_path):
    try:
        edge_options = Options()
        edge_driver_path = r"D:\edgedriver_win64\msedgedriver.exe"
        service = Service(edge_driver_path)
        driver = webdriver.Edge(service=service, options=edge_options)

        cookies = []
        for cookie_str in headers["cookie"].split('; '):
            name, value = cookie_str.split('=', 1)
            cookies.append({'name': name, 'value': value})

        driver.get('https://pixabay.com/')
        for cookie in cookies:
            driver.add_cookie(cookie)

        driver.get(url)
        random_seconds = random.randint(5, 10)
        time.sleep(random_seconds)

        redirected_url = driver.current_url
        driver.quit()

        response = requests.get(redirected_url, headers=headers)
        response.raise_for_status()

        with open(save_path, 'wb') as file:
            file.write(response.content)
        logger.info(f"图片下载成功，保存路径为: {save_path}")
        return True
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP 错误发生: {http_err}")
        return False
    except Exception as err:
        logger.error(f"发生其他错误: {err}")
        return False


if __name__ == "__main__":
    try:
        connection = mysql.connector.connect(
            host='192.168.10.70',
            user='root',
            password='zq828079',
            database='data_sql'
        )
        cursor = connection.cursor()

        query = "SELECT title, category, download_link FROM pixabay_pic WHERE download_state = FALSE"
        cursor.execute(query)
        rows = cursor.fetchall()

        for title, category, download_link in rows:
            output_path = rf"E:\pix 3.28图片下载{category}"
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            file_name = f'{title}.jpg'
            save_path = os.path.join(output_path, file_name)
            if os.path.exists(save_path):
                logger.info(f"{title}已下载，跳过")
                continue

            logger.info(f"下载链接：{download_link}")
            if download_image(download_link, save_path):
                update_query = "UPDATE pixabay_pic SET download_state = TRUE WHERE title = %s"
                cursor.execute(update_query, (title,))
                connection.commit()

        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        logger.error(f"数据库错误: {err}")
    except Exception as err:
        logger.error(f"发生其他错误: {err}")