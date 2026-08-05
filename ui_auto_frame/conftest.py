import time
import pytest
from utils.driver_utils import get_driver
from utils.mysql_utils import execute_sql_file


@pytest.fixture(scope="function")
def data_init_and_destory():
    # 音乐任务平台用例依赖前端「重置数据」，不走 WMS 库初始化
    from config.config import EXCEL_FILE
    if "音乐任务管理平台" in EXCEL_FILE:
        yield
        return
    # 测试函数调用效果
    execute_sql_file('./mysql_data_init/fuction.sql', 'INIT_WAREHOUSE_AREA')
    yield
    # 销毁数据，执行销毁文件
    execute_sql_file("./mysql_data_init/destroy.sql", "DESTROY")


@pytest.fixture(scope="function")
def driver_handler():

    # 创建浏览器对象
    driver = get_driver()
    # yield两大作用：1.暂停并恢复执行。2.返回值给调用者，但不中止函数
    # 如果想要把返回值传递到测试函数中，最简单的办法就是在测试函数显示调用这个夹具
    yield driver
    # 关闭浏览器
    driver.quit()


# pytest_runtest_makereport是pytest内置的钩子函数，每条用例前后自动执行，用于生成测试用例的执行结果(skipped/failed/passed等)
# 带上 @pytest.hookimpl(hookwrapper=True)，表示可以前后夹击(自定义修改结果outcome)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # item: 测试用例对象本身（一条），包括测试类/参数化信息/标记/所在文件路径等
    # call: 测试用例执行过程信息，包括执行阶段，执行开始和结束时间，执行结果等

    outcome = yield  # 必须通过yield获取原始流程的结果
    res = outcome.get_result()

    # 可以通过打印来观察一下钩子函数的执行效果
    # print(res)

    # 如果执行过程中发现执行失败了
    if res.when == "call" and res.failed:
        # 从测试用例对象中获取所有参数
        params = item.funcargs
        # print(params)

        driver = params["driver_handler"]
        now_time = time.strftime("%Y-%m-%d %H_%M_%S")
        driver.save_screenshot(f"./screenshot/失败用例_{params['case']['id']}_{params['case']['title']}_{now_time}.png")
