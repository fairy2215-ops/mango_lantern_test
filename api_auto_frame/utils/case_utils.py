"""用例字段渲染与安全解析（替代 eval）。"""
import json
import logging

from jinja2 import Template


def render_case(case, context):
    """对用例中的字符串字段做 Jinja2 变量替换，如 {{TOKEN}}。"""
    rendered = {}
    for key, value in case.items():
        if isinstance(value, str) and value:
            rendered[key] = Template(value).render(**context)
        else:
            rendered[key] = value
    return rendered


def parse_obj(value, field_name=""):
    """把 Excel 中的 JSON 字符串安全转成 dict/list；空值返回 None。"""
    if value is None or value == "":
        return None
    if isinstance(value, (dict, list)):
        return value
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"字段 [{field_name}] 不是合法 JSON，请使用双引号。原始值: {value}"
        ) from exc


def parse_files(value):
    """
    文件上传字段解析。
    Excel 示例: {"file": ["1.jpg", "file/1.jpg", "image/jpeg"]}
    """
    parsed = parse_obj(value, "files")
    if not parsed:
        return None

    files = {}
    for key, item in parsed.items():
        if isinstance(item, list) and len(item) >= 2:
            filename, path = item[0], item[1]
            content_type = item[2] if len(item) > 2 else None
            file_obj = open(path, "rb")
            files[key] = (filename, file_obj, content_type) if content_type else (filename, file_obj)
        elif isinstance(item, str):
            files[key] = open(item, "rb")
        else:
            raise ValueError(f"files 字段格式不正确: {key}={item}")
    return files


def jsonpath_first(data, expr, field_name="jsonpath"):
    """安全取 jsonpath 第一个结果，未命中时抛出明确错误。"""
    import jsonpath

    result = jsonpath.jsonpath(data, expr)
    if not result:
        logging.error(f"{field_name} 未匹配到数据，表达式: {expr}，响应: {data}")
        raise AssertionError(f"{field_name} 未匹配到数据，表达式: {expr}")
    return result[0]
