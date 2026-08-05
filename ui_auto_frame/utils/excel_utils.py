import openpyxl

from config.config import *


def read_excel():
    # 打开 excel 文件
    workbook = openpyxl.load_workbook(( EXCEL_FILE ))   # 参数：文件路径

    # 选择表
    worksheet = workbook[SHEET_NAME]

    # 读数据操作
    data = []
    # 先把所有用例数据读出来，再进行筛选，合格的用例放到最终结果data中
    all_cases = []
    # 定义当前用例数据，按条处理用例
    current_case = None

    # 设置循环，遍历所有表
    for worksheet in workbook.worksheets:

        keys = [cell.value for cell in worksheet[2]]   # 拿key行，即第二行，生成一个列表
        for row in worksheet.iter_rows(min_row=3,values_only=True):
            dict_data = dict(zip(keys,row))   # 将字段和值组装成字典
            # if dict_data["is_true"]:   #每次循环都判断用例中的每条用例需不需要执行，执行才添加本次组装的数据
            # 用例中的id字段不为空，则判断为新的一条用例
            if dict_data["id"]is not None:
                # 组织用例的规则：新的用例组织全部信息，旧的用例组织部分信息（在下方添加）
                current_case = {
                    "id":dict_data["id"],
                    "feature":dict_data["feature"],
                    "story": dict_data["story"],
                    "title":dict_data["title"],
                    "steps":[{
                        "step_num":dict_data["step_num"],
                        "step_name":dict_data["step_name"],
                        "keyword":dict_data["keyword"],
                        "by":dict_data["by"],
                        "value":dict_data["value"],
                        "data":dict_data["data"],
                        "index":dict_data["index"]
                    }],
                    "is_true":dict_data["is_true"],
                }
                all_cases.append(current_case)
            # id为空且上一条用例存在，则添加用例的步骤
            elif current_case is not None:
                current_case["steps"].append({"step_num":dict_data["step_num"],
                        "step_name":dict_data["step_name"],
                        "keyword":dict_data["keyword"],
                        "by":dict_data["by"],
                        "value":dict_data["value"],
                        "data":dict_data["data"],
                        "index":dict_data["index"]})
    # 过滤数据，只保留is_true为True的用例
    data = [case for case in all_cases if case["is_true"]]
    # print(data)
    # 关闭 excel 文件
    workbook.close()
    return data
