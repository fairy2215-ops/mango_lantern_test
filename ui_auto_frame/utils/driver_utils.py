import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from config.config import *


# 根据配置项实现：创建哪种浏览器对象，使用哪种驱动管理方式，是否开启无头模式
def get_driver():
    # 初始化driver
    driver = None
    # 判断浏览器类型
    if BROWSER_TYPE == "chrome":
        driver = get_chrome_driver()
    if BROWSER_TYPE == "edge":
        driver = get_edge_driver()
    return driver


def get_chrome_driver():
    # 不论用哪种驱动模式，都需要先设置浏览器参数
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    # 判断是否开启无头模式
    if HEADLESS:
        options.add_argument("--headless")

    # 判断是否使用远程浏览器驱动
    if DRIVER_TYPE == "local":
        service = Service(CHROME_DRIVER_PATH)
    else:
        service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(options=options, service=service)
    logging.info("启动chrome浏览器成功")
    return driver


def get_edge_driver():
    options = webdriver.EdgeOptions()
    options.add_argument("--start-maximized")

    # 判断是否开启无头模式
    if HEADLESS:
        options.add_argument("--headless")

    # 判断是否使用远程浏览器驱动
    if DRIVER_TYPE == "local":
        service = EdgeService(EDGE_DRIVER_PATH)
    else:
        service = EdgeService(EdgeChromiumDriverManager().install())

    driver = webdriver.Edge(options=options, service=service)
    logging.info("启动edge浏览器成功")
    return driver
