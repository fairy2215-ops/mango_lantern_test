from functools import wraps

import allure
import logging

# 定义装饰器
def kw_step(func):
    # 使用tunctools.wraps保留原函数名
    @wraps(func)
    def wrapper(self, step):
        # 使用 allure.step 记录步骤信息
        with allure.step(f"第{step['step_num']}步：{step['step_name']}"):
            # 使用 Logging.info 输出日志
            logging.info(f"第{step['step_num']}步：{step['step_name']} - 元素({step['by']},{step['value']})，操作数据：{step['data']}")
            # 调用被装饰的函数
            return func(self, step)
    return wrapper