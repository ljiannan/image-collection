import time
from urllib.parse import unquote, urlsplit, parse_qs
import requests
import os
import mysql.connector
import logging
from urllib.parse import unquote
from datetime import datetime


headers = {
    # "accept": "*/*",
    # "accept-encoding": "gzip, deflate, br, zstd",
    # "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "content-type": "application/json",
    "cookie": "_fbp=fb.1.1740644381892.22830351949064128; pexels_message_banner_creative-rituals-2025=1; _hjSessionUser_171201=eyJpZCI6IjZmZGJkNTI5LTFjNDItNTc2Mi04MzdmLWNmNjllYzc3YTEzZSIsImNyZWF0ZWQiOjE3NDA2NDQzNzA4MDQsImV4aXN0aW5nIjp0cnVlfQ==; __cf_bm=ewMgDctRGw6pWr2okH307HbJibq3y61AqVcfQTNHn_s-1741137444-1.0.1.1-6tyepLmp3ewJ_a0nUfgbInfmopb_BDucb6cfxEBRo8MJgF2f95Hz7xBx0h8ZSYrlYCjWrVg1dc.h7nn9B_1JCxry9raQT5KCUqgrcfBzNj0; _cfuvid=rzefsCE5ovlEZ3y_dERsJCAjqAShDmEE0C4Qze_PfvI-1741137444663-0.0.1.1-604800000; _sp_ses.9ec1=*; country-code-v2=CN; cf_clearance=sGaznpWekBUSTxOxlT60O7ZJJa0tXtyK_nFADF2yT_g-1741137448-1.2.1.1-bi.1.ZKsNj.tpryWpxywNQ3Qb8gT9y1F7S0O4lFdRI9hrNVt1ATTbUeAo49qrU1gHoTubbWxjDH1HMtJ0Iqy5408YZSGGyTtbg9uhEFLkj9.7BW5AwKTgW75iue7cOMrKRYWknBTuNVJ_9g7JZ1OPCXfP6tkBUgwNaYeiBioH729jvFlp0ytiRa3aNWHEovg5l0owOcIbEhBhRZAWpMbdTLtYJ4XKwvXELvvJsgtWzRoZMMhPrOzytFXJR6i3gueLC5gi_HJ8JbqKTZYW50tq1Dwr5rxxJHUAOwd.Smif_BJShYV9K._YgkCMPp5JKXCZFcitvhCNxKssFQx_inpvNJVpH9c4E2qUNJ6HaJyi9Z7pMyq15X7bBUSZvfpHizqjYOwNuDna8DZb9FK6Kbzq.C.OoSVnJ1v8g22boNHUYs; _hjSession_171201=eyJpZCI6ImEyZjRmYjhlLTNmZTUtNGY0NS1iZDdiLTg1ZjRhMzQ2ZWI2ZiIsImMiOjE3NDExMzc0NTE4NTUsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; _gid=GA1.2.1332797806.1741137539; OptanonAlertBoxClosed=2025-03-05T01:19:03.120Z; _ga=GA1.1.449538479.1740644369; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Mar+05+2025+09%3A20%3A52+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202301.1.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=CN%3BTJ; _ga_8JE65Q40S6=GS1.1.1741137450.2.1.1741137659.0.0.0; _sp_id.9ec1=ddaf142a-e7d7-4159-b6ce-c654ef25dfc2.1740644368.2.1741137746.1740646115.d3d1ff66-4bbb-46f2-9a2a-9f9c33e5028b.532fc1cf-76b5-459f-98fc-0c9df506964d.e5f30f40-11d3-4c5e-9600-181ffeb13c97.1741137448194.31; _dd_s=rum=2&id=1b8418c1-dbb0-461e-bf62-7d6acfea0696&created=1741137447696&expire=1741138657628",
    "priority": "u=1, i",
    "referer": "https://www.pexels.com/search/man/",
    "sec-ch-ua": '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "secret-key": "H2jk9uKnhRmL6WPwh89zBezWvr",
    "traceparent": "00-0000000000000000b547d24c9268aa63-574e0b40417ecd22-01",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
    "x-client-type": "react",
    "x-forwarded-cf-connecting-ip": "",
    "x-forwarded-cf-ipregioncode": "",
    "x-forwarded-http_cf_ipcountry": ""
}

# ===================== Logo展示 =====================
print(f"{'*' * 40}")
print(f"* Pexels图片采集器启动")
print(f"* 启动时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"{'*' * 40}\n")
# ===================================================

# ===================== 配置区域 =====================
# 更新为六大类关键词 (人物/动物/植物/建筑/食物/交通工具)
keywords = [
    # People
    # "man", "woman", "child", "baby", "teenager",
    # "elderly", "couple", "family", "friends", "crowd",
    # "athlete", "actor", "actress", "teacher", "doctor",
    # "scientist", "artist", "pilot", "waiter", "nurse",

    # Animals
    # "dog", "cat", "elephant", "lion", "tiger",
    # "giraffe", "monkey", "kangaroo", "panda", "koala",
    # "bird", "fish", "dolphin", "whale", "snake",
    # "crocodile", "horse", "sheep", "cow", "rabbit",

    # Plants
    # "flower", "tree", "leaf", "grass", "forest",
    # "garden", "cactus", "succulent", "bonsai", "orchid",
    # "rose", "lily", "sunflower", "tulip", "daffodil",
    # "fern", "bamboo", "mushroom", "aloe", "ivy",

    # Buildings
    # "building", "skyscraper", "house", "castle", "bridge",
    # "temple", "church", "mosque", "office", "mall",
    # "school", "hospital", "library", "museum", "theater",
    # "factory", "warehouse", "stadium", "tower", "lighthouse",

    # Foods
    # "pizza", "hamburger", "noodles", "rice", "sushi",
    # "cake", "ice - cream", "chocolate", "salad", "sandwich",
    # "steak", "fish and chips", "pasta", "dumplings", "baozi",
    # "soup", "dessert", "fruit", "vegetable", "seafood",

    # Vehicles
    # "car", "bus", "train", "plane", "ship",
    # "bicycle", "motorcycle", "truck", "subway", "helicopter",
    # "tractor", "fire truck", "ambulance", "taxi", "ferry",
    # "hot - air balloon", "spacecraft", "rocket", "scooter", "skateboard"
    # 植物笼统概括关键词
    # "plant", "flora", "vegetation"
    # ... existing code ...
    # 原有的其他类别关键词...
    # 新增建筑相关笼统关键词
    "architecture",
    "historic architecture",
    "modern architecture",
    "contemporary architecture",
    "urban architecture",
    "rural architecture",
    "residential architecture",
    "commercial architecture",
    "public architecture",
    "sacred architecture",
    "landmark building",
    "iconic architecture",
    "architectural complex",
    "skyscraper cluster",
    "old building",
    "new building",
    "tall building",
    "low-rise building",
    "unique architecture",
    "stunning architecture"
# ... existing code ...
]
out_path = fr"E:\pix 4.2图片下载\建筑"  # 图片保存路径

page_start= 1  # 开始页数
page_add = 200
mysql_config = {
    'user': 'root',
    'password': 'zq828079',
    'host': '192.168.10.70',
    'database': 'data_sql'
}

# ===================================================


# ===================== 日志配置 =====================
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.FileHandler(f'pexels_crawler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
# ===================================================


def create_table(cursor):
    """创建数据库表"""
    try:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS pexels_pic (
                id INT AUTO_INCREMENT PRIMARY KEY,
                image_name VARCHAR(255) NOT NULL,
                category VARCHAR(50) DEFAULT NULL,
                description TEXT,
                download_link VARCHAR(255) UNIQUE
            )
        """)
        logger.info("数据库表创建/验证成功")
    except Exception as e:
        logger.error(f"数据库表创建失败: {str(e)}")
        raise


def get_filename_from_url(url):
    """从下载链接的dl参数中提取文件名"""
    try:
        # 解码URL
        decoded_url = unquote(url)
        logger.debug(f"原始URL: {decoded_url}")

        # 拆分URL路径和参数
        parsed = urlsplit(decoded_url)
        query_params = parse_qs(parsed.query)

        # 优先从dl参数获取文件名
        if 'dl' in query_params:
            filename = query_params['dl'][0]  # 取第一个dl参数值
            logger.debug(f"从dl参数获取文件名: {filename}")
        else:
            # 回退方案：从路径获取文件名
            filename = parsed.path.split('/')[-1]
            logger.debug(f"从路径获取文件名: {filename}")

        # 安全处理文件名（移除路径分隔符）
        filename = filename.split('/')[-1]
        return filename

    except Exception as e:
        logger.warning(f"文件名解析失败: {str(e)}")
        return f"unknown_{int(datetime.now().timestamp())}.jpg"


def download_image(url, save_path):
    """下载图片到本地"""
    try:
        logger.info(f"开始下载: {url}")
        if os.path.exists(save_path):
            logger.info("链接已下载，跳过")
        else:
            response = requests.get(url, stream=True, timeout=30)

            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                logger.info(f"下载成功: {save_path}")
                return True

            logger.error(f"下载失败 HTTP状态码: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"下载异常: {str(e)}")
        return False


def get_existing_links():
    """获取数据库中已存在的所有下载链接"""
    try:
        with mysql.connector.connect(**mysql_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT download_link FROM pexels_pic")
                return {link[0] for link in cursor.fetchall()}
    except Exception as e:
        logger.error(f"获取已存在链接失败: {str(e)}")
        return set()


def process_page(page_num, keyword,existing_links):
    """处理单个页面（新增existing_links参数）"""
    logger.info(f"{'=' * 30} 开始处理{keyword}第 {page_num} 页 {'=' * 30}")
    url = f"https://www.pexels.com/en-us/api/v3/search/photos?query={keyword}&page={page_num}&per_page=24&orientation=all&size=all&color=all&sort=popular&seo_tags=true"
    output_path=os.path.join(out_path,f'{keyword}')
    os.makedirs(output_path,exist_ok=True)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"页面请求失败: {str(e)}")
        return existing_links  # 返回更新后的链接集合

    if response.status_code == 200:
        try:
            data = response.json()
            results = []
            new_links = set()

            for idx, item in enumerate(data["data"], 1):
                try:
                    download_link = item["attributes"]["image"]["download_link"]

                    # 检查链接是否已存在
                    if download_link in existing_links:
                        logger.warning(f"链接重复，跳过: {download_link}")
                        continue

                    description = item["attributes"].get("description", "")
                    filename = get_filename_from_url(download_link)
                    save_path = os.path.join(output_path, filename)

                    # 下载图片
                    download_success = False
                    if not os.path.exists(save_path):
                        download_success = download_image(download_link, save_path)
                    else:
                        logger.info(f"文件已存在: {filename}")
                        download_success = True

                    if download_success:
                        record = (filename, keyword, description, download_link)
                        results.append(record)
                        new_links.add(download_link)
                        logger.debug(f"记录添加成功: {filename}")
                    else:
                        logger.warning(f"跳过未下载文件: {filename}")

                except KeyError as e:
                    logger.warning(f"数据字段缺失: {str(e)}")
                    continue

            if results:
                try:
                    with mysql.connector.connect(**mysql_config) as conn:
                        with conn.cursor() as cursor:
                            create_table(cursor)
                            sql = """
                                INSERT IGNORE INTO pexels_pic 
                                (image_name, category, description, download_link)
                                VALUES (%s, %s, %s, %s)
                            """
                            cursor.executemany(sql, results)
                            conn.commit()
                            inserted = cursor.rowcount
                            existing_links.update(new_links)  # 更新已存在链接集合
                            logger.info(f"成功插入 {inserted} 条记录")
                except mysql.connector.Error as e:
                    logger.error(f"数据库操作失败: {str(e)}")
            else:
                logger.warning("当前页面没有有效数据")

        except ValueError:
            logger.error("JSON解析失败")
    else:
        logger.error(f"请求失败 HTTP {response.status_code}")

    return existing_links  # 返回更新后的链接集合


# ===================== 主程序 =====================
if __name__ == "__main__":
    os.makedirs(out_path, exist_ok=True)
    logger.info(f"输出目录已准备: {out_path}")

    try:
        # 初始化时获取所有已存在的链接
        existing_links = get_existing_links()
        logger.info(f"已加载 {len(existing_links)} 条历史记录")
        for keyword in keywords:
            for page_num in range(page_start, page_start+page_add):
                existing_links = process_page(page_num, keyword,existing_links)

                # 添加适当延迟
                if page_num % 5 == 0:
                    logger.info(f"已完成 {page_num} 页，暂停5秒...")
                    time.sleep(5)
                else:
                    time.sleep(1)

    except KeyboardInterrupt:
        logger.warning("用户中断操作！")
    except Exception as e:
        logger.critical(f"程序异常终止: {str(e)}", exc_info=True)
    finally:
        logger.info("程序运行结束\n")