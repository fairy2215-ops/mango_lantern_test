import os

# 环境基准地址（可用环境变量覆盖）
BASE_URL = os.getenv("BASE_URL", "http://localhost:3000")

# excel 格式的测试用例文件配置
EXCEL_FILE = os.getenv("EXCEL_FILE", "./data/mtm_api_cases.xlsx")
SHEET_NAME = os.getenv("SHEET_NAME", "Sheet1")

# 请求超时（秒）
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))

# mysql 配置
DB_HOST = os.getenv("DB_HOST", "192.168.10.131")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "mydb")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")
DB_CHARSET = os.getenv("DB_CHARSET", "utf8")

# 清除冗余数据（按需在 conftest 中使用）
SQL1 = os.getenv("SQL1", "")
SQL2 = os.getenv("SQL2", "")
SQL3 = os.getenv("SQL3", "")
