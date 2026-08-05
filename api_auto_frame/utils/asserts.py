import logging

import allure
import jsonpath

from utils.send_request import send_jdbc_request


@allure.step("步骤3：HTTP响应断言")
def http_assert(case, res, index=0):
    expected_status = case.get("status_code")
    if expected_status is None or expected_status == "":
        expected_status = 200
    expected_status = int(expected_status)
    logging.info(
        f"HTTP状态码断言：实际结果（{res.status_code}）==预期结果（{expected_status}）"
    )
    assert res.status_code == expected_status, (
        f"状态码不一致: 实际={res.status_code}, 预期={expected_status}, body={res.text}"
    )

    check = case.get("check")
    expected = case.get("expected")
    if check:
        try:
            body = res.json()
        except ValueError as exc:
            raise AssertionError(f"响应不是 JSON，无法按 check 断言: {res.text}") from exc

        matched_list = jsonpath.jsonpath(body, check)
        if not matched_list:
            raise AssertionError(f"check 未匹配到数据，表达式: {check}，body={res.text}")
        matched = matched_list[index]
        logging.info(f"HTTP响应断言内容：实际结果（{matched}）==预期结果（{expected}）")
        assert matched == expected, (
            f"响应断言失败: 实际={matched}, 预期={expected}, check={check}"
        )
    elif expected is not None and expected != "":
        logging.info(f"HTTP响应断言内容：预期结果（{expected}） in （实际结果{res.text}）")
        assert str(expected) in res.text, (
            f"模糊断言失败: 预期片段={expected}, body={res.text}"
        )


def jdbc_assert(case):
    if case.get("sql_check") and case.get("sql_expected") is not None:
        with allure.step("步骤3：JDBC响应断言"):
            result = send_jdbc_request(case["sql_check"])
            logging.info(
                f"JDBC响应断言内容：实际结果（{result}） == （预期结果{case['sql_expected']}）"
            )
            assert result == case["sql_expected"]
