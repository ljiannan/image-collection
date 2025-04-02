#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/3/12 10:46
# @Author  : CUI liuliu
# @File    : pixabay_api_pic.py

import logging
import os
import random
import time
import requests
import mysql.connector

mysql_config = {
    'user': 'root',
    'password': 'zq828079',
    'host': '192.168.10.70',
    'database': 'data_sql'
}
keyword = "man"
page_start = 1
total_pages = 200  # 爬取总页数
# ===================================================

# ================日志配置============================
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.FileHandler(f'pixabay_pic_{keyword}.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "max-age=0",
    "cookie": "is_human=1; anonymous_user_id=74dbd8746a0d43898058f10f83ff4b09; csrftoken=r7klvy4kC0sbUlmBkUQE8kxlriAMTD3w; lang=zh; dwf_search_ai_tags=True; __cf_bm=WTprgnbkXIKJm4lgwFpZSip0hzJqJvy3.cTWNx8DRvI-1741226894-1.0.1.1-ZAlIjwJ.JXOS.r9occOVmHMEZMe0q3WVm2hGrfZjMizcjXZ0tpSKK1HbVaaAK_f_wMGmex76ZwuX30Lj5u3oV8Yd0l5Sz3rgfpCKw1VkLO0; _sp_ses.aded=*; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Mar+06+2025+10%3A08%3A42+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202401.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=291064c1-cb85-4a96-ad8c-a34ccfed3103&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false; _sp_id.aded=62825686-cb0f-4635-9447-03c63aa6a34f.1741139799.6.1741226983.1741167724.530f4666-315d-42e7-b415-9db961f0a959.e1766517-2bd5-494a-aee1-5b4ba66d085a.fd8e567c-7bcf-4b8c-887a-f99def820bf5.1741226927807.4",
    "priority": "u=0, i",
    "referer": "https://pixabay.com/zh/photos/",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Microsoft Edge\";v=\"133\", \"Chromium\";v=\"133\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"
}


def create_table(cursor):
    """创建数据库表"""
    try:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS pixabay_pic (
                id INT AUTO_INCREMENT PRIMARY KEY,
                page_id VARCHAR(255) NOT NULL,  
                title VARCHAR(255) NOT NULL,
                tags VARCHAR(255) NOT NULL,
                page_link VARCHAR(255) UNIQUE,
                download_link VARCHAR(255),
                download_state BOOLEAN DEFAULT FALSE NOT NULL
            )
        """)
        logger.info("数据库表创建/验证成功")
    except Exception as e:
        logger.error(f"数据库表创建失败: {str(e)}")
        raise

def insert_data(cursor, page_id, page_link, tags, title, download_link):
    """插入数据到数据库"""
    try:
        sql = """
            INSERT INTO pixabay_pic (page_id, page_link, tags, title, download_link)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE page_id=VALUES(page_id), page_link=VALUES(page_link), tags=VALUES(tags), title=VALUES(title), download_link=VALUES(download_link)
        """
        cursor.execute(sql, (page_id, page_link, tags, title, download_link))
        logger.info(f"插入成功: {title}")
    except Exception as e:
        logger.error(f"插入失败: {str(e)}")

def main():
    try:
        # 初始化数据库连接
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        create_table(cursor)
        logger.info("数据库连接成功！")
        for page_num in range(page_start, page_start + total_pages):
            url = f'https://pixabay.com/api/?key=49182352-52458db6c869991d508cf7fa4&q={keyword}&image_type=photo&pretty=true&page={page_num}&per_page=10'
            logger.info(f"正在处理第 {page_num} 页: {url}")
            api_response = requests.get(url, headers=headers)
            api_response.raise_for_status()
            data = api_response.json()
            items = data["hits"]
            for item in items:
                pic_id = item.get("id")
                pageurl = item.get("pageURL")
                tags = item.get("tags")
                parts = pageurl.split('/')
                image_part = parts[-2]
                title = image_part
                download_link = f"https://pixabay.com/images/download/{image_part}.jpg"

                logger.info("图片ID: %s, 页面URL: %s, 标签: %s, 标题: %s, 下载链接: %s", pic_id, pageurl, tags, title,
                            download_link)
                insert_data(cursor, pic_id, pageurl, tags, title, download_link)
            conn.commit()  # 提交事务
            time.sleep(10)
    except Exception as e:
        logger.error(f"主循环异常: {str(e)}", exc_info=True)
    finally:
        # 关闭资源
        cursor.close()
        conn.close()
        logger.info("数据库连接已关闭")

if __name__ == "__main__":
    main()