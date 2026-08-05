import logging
import pytest
from jinja2 import Template

from core.assert_keywords import AssertKeywords
from core.business_keywords import BusinessKeywords
from core.keywords import Keywords
from utils.allure_utils import allure_init
from utils.excel_utils import read_excel


class TestRunner:

    # 读取测试用例文件中的全部数据，用属性保存即可
    data = read_excel()

    # 提取后的数据需要初始化一个全局的属性来保存，可以使用{}空字典
    all = {}   # 全局类属性
    # 这个装饰器是把 data 里边的每一条用例给到这个 case，然后再把这个 case 给到方法里边的参数case，装饰器参数名字要和方法的参数名相同。
    # 失败用例自动重跑：最多重试 3 次，每次重试间隔 3 秒
    # @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize("case",data)
    def test_case(self, case, driver_handler, data_init_and_destory):

        # 引用全局类属性 all
        all = self.all

        # 初始化 allure 报告，给 allure_init（）函数传参，传case
        allure_init(case)

        # 0.测试用例的描述信息日志
        logging.info(f'用例ID:{case["id"]}  模块：{case["feature"]}  场景:{case["story"]}  标题：{case["title"]}')

        # 创建关键字对象
        keywords = Keywords(driver_handler)    # 操作类关键字（打开、点击、输入等）
        assert_keywords = AssertKeywords(driver_handler)   # 断言类关键字（验证URL、标题等）
        business_keywords = BusinessKeywords(driver_handler)   # 业务关键字（登录）

        # 执行每一个步骤
        for step in case["steps"]:
            # str(step) - 把步骤字典转换成字符串
            # Template(...) - 用Jinja2创建模板对象，识别其中的{{变量名}}
            # .render(all) - 用全局变量all中的值替换模板中的{{变量名}}
            # eval(...) - 把渲染后的字符串再转换回字典
            step = eval(Template(str(step)).render(all))

            # for....else 语法：如果没有遇到break则执行else中的代码, 如果遇到break则跳过else
            # 按步骤划分，每个步骤都去查找一次keywords和assert_keywords
            for i in [keywords, assert_keywords, business_keywords]:
                # 使用hasattr判断关键字是否存在
                if hasattr(i, step["keyword"]):
                    # func_name 现在是一个"绑定方法对象"，例如：等价于func_name = keywords.input这个方法
                    func_name = i.__getattribute__(step["keyword"])
                    # 特殊业务处理，如果找到关键字为get_attribute，则将返回值保存到全局类属性all中
                    if func_name.__name__ == "get_attribute":
                        key, value = func_name(step)
                        all[key] = value
                    else:
                        func_name(step)
                    break
            # for...else...语法: 如果没有遇到break则执行else中的代码, 如果遇到break则跳过else
            else:
                raise AttributeError(f"❌未找到关键字: {step['keyword']}")

