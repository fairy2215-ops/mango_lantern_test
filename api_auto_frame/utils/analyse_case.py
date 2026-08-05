# 功能：解析请求数据（使用 json.loads，不再使用 eval）
import logging

import allure

from config.config import BASE_URL
from utils.case_utils import parse_files, parse_obj


@allure.step("步骤1：解析请求数据")
def analyse_case(case):
    method = case["method"]
    url = BASE_URL + case["path"]
    headers = parse_obj(case.get("headers"), "headers")
    params = parse_obj(case.get("params"), "params")
    data = parse_obj(case.get("data"), "data")
    json_body = parse_obj(case.get("json"), "json")
    files = parse_files(case.get("files"))

    request_data = {
        "method": method,
        "url": url,
        "headers": headers,
        "params": params,
        "data": data,
        "json": json_body,
        "files": files,
    }
    logging.info(f"请求数据为：{request_data}")
    allure.attach(f"请求数据为：{request_data}", name="解析数据结果")
    return request_data
