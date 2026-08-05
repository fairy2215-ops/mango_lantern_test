import allure


def allure_init(case):
    # 初始化allure报告,在模型渲染之后进行
    allure.dynamic.feature(case["feature"])
    allure.dynamic.story(case["story"])
    # allure.dynamic.title(case["title"])
    # 下面是用到了f-string 格式化语法，用 f"字符串内容{变量/表达式}" 形式，直接在字符串里嵌入变量或表达式的值。
    allure.dynamic.title(f"ID:{case["id"]}--{case["title"]}")
