import os

import pytest

from config.config import MULTI_PROCESS

# os.system(命令) 相当于在cmd中执行命令
if __name__ == "__main__":
    # 判断是否多进程执行
    if MULTI_PROCESS:
        pytest.main(["-vs",
                     "-nauto",   # "-nauto" 多进程，自动分配核心数
                     "./testcases/test_runner.py",
                     "--alluredir", "./report/test/json_report",   # 指定一个目录，并生成中间结果
                     "--clean-alluredir"])   # --clean-alluredir 每次运行会清空中间结果
    else:
        pytest.main(["-vs",
                     "./testcases/test_runner.py",
                     "--alluredir", "./report/test/json_report",
                     "--clean-alluredir"])
    # allure generate 中间结果目录 -o 目标html报告的目录 --clean
    os.system("allure generate ./report/test/json_report -o ./report/test/html_report --clean")
    # 生成后自动打开 allure 报告（会启动本地服务并拉起浏览器）
    os.system("allure open ./report/test/html_report")
