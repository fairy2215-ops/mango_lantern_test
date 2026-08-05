import logging

import allure
import pymysql
import requests

from config.config import (
    DB_CHARSET,
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
    REQUEST_TIMEOUT,
)


@allure.step("步骤2：发起请求")
def send_http_request(**request_data):
    request_data.setdefault("timeout", REQUEST_TIMEOUT)
    res = requests.request(**request_data)
    logging.info(f"发送HTTP请求，状态码={res.status_code}，响应文本为：{res.text}")
    allure.attach(
        f"status={res.status_code}\n{res.text}",
        name="HTTP请求的响应",
    )
    return res


def send_jdbc_request(sql, index=0):
    conn = pymysql.Connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        charset=DB_CHARSET,
    )
    cur = conn.cursor()
    try:
        cur.execute(sql)
        result = cur.fetchone()
        if not result:
            raise AssertionError(f"SQL未查询到数据: {sql}")
        return result[index]
    finally:
        cur.close()
        conn.close()
