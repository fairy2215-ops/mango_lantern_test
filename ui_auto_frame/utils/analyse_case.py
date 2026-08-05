#功能：解析请求数据
#test_runner会对excel用例进行读取，但是用例中的数据读取过来是字符型
# 需要转换成字典类型，用到eval（）函数,然后使用一个变量把转化完的数据组装起来
    #eval（）去掉字符串的双引号，并对能计算的内容进行计算
import logging

import allure
from config.config import BASE_URL


#优化allure报告，使用allure.step（“步骤描述”）装饰器标记函数，会显示在allure报告中
@allure.step("步骤1：解析请求数据")
def analyse_case(case):
    method = case["method"]
    url = BASE_URL + case["path"]
    #三元表达式：if...else...的简写：变量 = 结果1 if 条件成立 else 结果2
    headers = eval(case["headers"]) if isinstance(case["headers"], str) else None
    params = eval(case["params"]) if isinstance(case["params"], str) else None
    data = eval(case["data"]) if isinstance(case["data"], str) else None
    json = eval(case["json"]) if isinstance(case["json"], str) else None
    files = eval(case["files"]) if isinstance(case["files"], str) else None

    request_data = {
        "method": method,
        "url": url,
        "headers": headers,
        "params": params,
        "data": data,
        "json": json,
        "files": files
    }
    # 1.组装数据日志
    logging.info(f"请求数据为：{request_data}")
    allure.attach(f"请求数据为：{request_data}",name="解析数据结果")
    #数据封装过来会影响test_runner中的request_data，要加返回值
    return request_data