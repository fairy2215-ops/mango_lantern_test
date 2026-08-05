import openpyxl


def read_excel(file_path, sheet_name):
    workbook = openpyxl.load_workbook(file_path)
    worksheet = workbook[sheet_name]

    data = []
    keys = [cell.value for cell in worksheet[2]]
    for row in worksheet.iter_rows(min_row=3, values_only=True):
        if not any(row):
            continue
        dict_data = dict(zip(keys, row))
        if not dict_data.get("id"):
            continue
        # is_true 为空时默认不执行；仅 True/1/"true" 执行
        flag = dict_data.get("is_true")
        if flag is True or flag == 1 or str(flag).lower() == "true":
            data.append(dict_data)

    workbook.close()
    return data
