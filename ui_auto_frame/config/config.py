# driver相关配置项

# 浏览器类型
BROWSER_TYPE = "chrome"
# 使用哪种浏览器驱动管理方式：local/remote
DRIVER_TYPE = "local"
# 本地浏览器驱动管理方式
CHROME_DRIVER_PATH = "./driver/chromedriver.exe"
EDGE_DRIVER_PATH = "./driver/msedgedriver.exe"
# 是否开启无头模式:TRUE/FALSE
HEADLESS = False
# excel格式的测试用例文件配置
EXCEL_FILE = "./data/音乐任务管理平台_关键字用例.xlsx"
SHEET_NAME = "Sheet1"
# 是否开启多线程测试
MULTI_PROCESS = False


# mysql配置
DB_HOST = "192.168.10.130"
DB_PORT = 3306
DB_NAME = "wms"
DB_USER = "root"
DB_PASSWORD = "123456"
