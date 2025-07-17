# -*- coding: utf-8 -*-
"""
Time:     2025/2/6 9:31
Author:   ZhaoQi Cao(czq)
Version:  V 0.2
File:     rename_file_all.py
Describe: 支持自定义起始编号，重命名为8位数字编号+原扩展名
"""
import os
import logging
import datetime

# 配置日志记录
def setup_logging(log_directory):
    """配置日志记录到文件."""
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)  # 创建日志目录
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_directory, f"rename_log_{timestamp}.log")
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    print(f"日志记录到: {log_file}")

def rename_files_and_folders_recursive(directory, counter=None):
    """
    递归地重命名指定目录及其子目录下的所有文件，按顺序排列，并记录日志。
    Args:
        directory: 要重命名的目录的路径。
        counter:  （可选）用于保持重命名计数的外部计数器。如果没有提供，函数将创建一个。
    """
    if counter is None:
        # 这里设置起始编号
        counter = {'value': START_NUMBER}  # 使用字典模拟可变整数，以便在递归调用中正确更新

    items = os.listdir(directory)
    items.sort()
    folders = [item for item in items if os.path.isdir(os.path.join(directory, item))]
    files = [item for item in items if os.path.isfile(os.path.join(directory, item))]

    for old_name in files:
        old_path = os.path.join(directory, old_name)
        ext = os.path.splitext(old_name)[1]
        new_name = str(counter['value']).zfill(8) + ext
        new_path = os.path.join(directory, new_name)
        temp_counter = counter['value']
        while os.path.exists(new_path):
            temp_counter += 1
            new_name = str(temp_counter).zfill(8) + ext
            new_path = os.path.join(directory, new_name)
        try:
            os.rename(old_path, new_path)
            logging.info(f"重命名: {old_name} -> {new_name}")
            print(f"重命名: {old_name} -> {new_name}")
            counter['value'] = temp_counter + 1
        except OSError as e:
            logging.error(f"重命名 {old_name} 出错: {e}")
            print(f"重命名 {old_name} 出错: {e}")

    for folder in folders:
        folder_path = os.path.join(directory, folder)
        rename_files_and_folders_recursive(folder_path, counter)

# ====== 这里设置参数 ======
directory_path = r"D:\图片暂存2"  # 替换为你的目录路径
log_directory = r"./logs"       # 替换为你的日志目录路径
START_NUMBER = 1833               # <<< 这里设置起始编号，比如从100开始就写100
# ========================

setup_logging(log_directory)
logging.info("开始递归重命名")
rename_files_and_folders_recursive(directory_path)
logging.info("递归重命名完成")
