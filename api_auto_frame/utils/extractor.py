import logging

import allure

from utils.case_utils import jsonpath_first, parse_obj
from utils.send_request import send_jdbc_request


def json_extractor(case, context, res):
    raw = case.get("jsonExData")
    if not raw:
        return
    with allure.step("步骤4：JSON提取"):
        try:
            body = res.json()
        except ValueError as exc:
            raise AssertionError(f"响应不是 JSON，无法提取: {res.text}") from exc

        for key, expr in parse_obj(raw, "jsonExData").items():
            context[key] = jsonpath_first(body, expr, field_name=f"jsonExData.{key}")
        logging.info(f"JSON提取，根据{raw}提取数据，此时上下文变量为：{context}")


def jdbc_extractor(case, context):
    raw = case.get("sqlExData")
    if not raw:
        return
    with allure.step("步骤4：JDBC提取"):
        for key, sql in parse_obj(raw, "sqlExData").items():
            context[key] = send_jdbc_request(sql)
        logging.info(f"JDBC提取，根据{raw}提取数据，此时上下文变量为：{context}")
