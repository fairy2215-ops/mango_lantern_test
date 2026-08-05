import jsonpath
import requests

login_data= {
    "method":"post",
    "url":"http://192.168.10.131:8888/api/private/v1/login",
    "params":None,
    "data": {"username":"admin","password":"123456"},
    "json":None,
    "files":None,
    "headers":None
}
upload_data= {
    "method":"post",
    "url":"http://192.168.10.131:8888/api/private/v1/upload",
    "params":None,
    "data": None,
    "json":None,
    "files":None,
    "headers":None
}
# 拿token
res1 = requests.request(**login_data)
# #注意注意：jsonpath返回的是列表，所以要加下标！！！
token = jsonpath.jsonpath(res1.json(),"$..token")[0]
print(token)

# 文件上传
# 1.带上token
upload_data["headers"] = {"Authorization":token}
# 2.设置上传数据 upload_data 中键名 files 的值
    # files 对应的值类似于{参数名：元组}
    # 参数值元组（参数1，参数2，参数3）
        # 第1个参数，上传服务器时用的文件名，如果没传，默认用 open（）函数中打开的文件的文件名
        # 第2个参数，用open（）函数打开的文件对象
        # 第3个参数，文件类型
upload_data["files"] = {"file":("1.jpg", open("../file/1.jpg", "rb"), "jpg")}
res2 = requests.request(**upload_data)
print(res2.json())
