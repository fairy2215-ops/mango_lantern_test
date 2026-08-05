import logging

import pytest

from config.config import EXCEL_FILE, SHEET_NAME
from utils.allure_utils import allure_init
from utils.analyse_case import analyse_case
from utils.asserts import http_assert, jdbc_assert
from utils.case_utils import render_case
from utils.excel_utils import read_excel
from utils.extractor import jdbc_extractor, json_extractor
from utils.send_request import send_http_request


class TestRunner:
    data = read_excel(EXCEL_FILE, SHEET_NAME)

    # 必须用类属性保存，pytest 每个用例都会 new 一个实例
    context = {}
    current_story = None
    failed_stories = set()

    @pytest.mark.parametrize("case", data)
    def test_case(self, case):
        story = case.get("story") or "default"

        if story in TestRunner.failed_stories:
            pytest.skip(f"同场景前置步骤失败，跳过: {story}")

        # 切换场景时清空上下文，避免变量串场景
        if story != TestRunner.current_story:
            TestRunner.context.clear()
            TestRunner.current_story = story

        try:
            case = render_case(case, TestRunner.context)
            allure_init(case)
            logging.info(
                f"用例ID:{case['id']}  模块：{case['feature']}  "
                f"场景:{case['story']}  标题：{case['title']}"
            )

            request_data = analyse_case(case)
            res = send_http_request(**request_data)
            http_assert(case, res)
            jdbc_assert(case)
            json_extractor(case, TestRunner.context, res)
            jdbc_extractor(case, TestRunner.context)
        except Exception:
            TestRunner.failed_stories.add(story)
            raise
