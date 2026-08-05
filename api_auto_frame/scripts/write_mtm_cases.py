"""将音乐任务管理平台业务场景用例改写为框架可用的 Excel 用例。"""
from openpyxl import Workbook

headers_cn = [
    "编号", "模块", "场景", "标题", "请求方式", "路径", "请求头", "url参数",
    "data参数", "json参数", "文件参数", "校验字段", "预期结果",
    "数据库校验内容", "数据库预期结果", "json提取", "sql提取", "是否执行",
]
headers_en = [
    "id", "feature", "story", "title", "method", "path", "headers", "params",
    "data", "json", "files", "check", "expected",
    "sql_check", "sql_expected", "jsonExData", "sqlExData", "is_true",
]

H_LIN = '{"x-test-user-id":"producer-lin","X-Test-User-Id":"producer-lin"}'
H_CHEN = '{"x-test-user-id":"producer-chen","X-Test-User-Id":"producer-chen"}'
H_ZHOU = '{"x-test-user-id":"reviewer-zhou","X-Test-User-Id":"reviewer-zhou"}'

LYRICS_OK = "这是一首关于海岸线的歌，海风吹过沙滩留下脚印与回声。"
LYRICS_FIX = "屏幕亮了又暗，未读消息停在凌晨两点半，我又写了一版新歌词内容。"
AUDIO_DEMO = "https://audio.example.com/demo.mp3"
AUDIO_FIX = "https://audio.example.com/fix.mp3"

DRAFT_OK = f'{{"lyrics":"{LYRICS_OK}","audioUrl":"{AUDIO_DEMO}"}}'
SUBMIT_OK = DRAFT_OK
DRAFT_FIX = f'{{"lyrics":"{LYRICS_FIX}","audioUrl":"{AUDIO_FIX}"}}'
SUBMIT_FIX = DRAFT_FIX
REVIEW_APPROVE = '{"decision":"APPROVE"}'
REVIEW_REJECT = '{"decision":"REJECT","reason":"歌词不完整请重写补充"}'

cases = [
    # 场景1：制作人主路径 领取 -> 草稿 -> 提交
    (
        1, "业务场景-制作人领取与制作提交", "场景1-主路径", "重置测试数据",
        "post", "/api/test/reset", None, None, None, None, None,
        "$..reset", True, None, None, None, None, True,
    ),
    (
        2, "业务场景-制作人领取与制作提交", "场景1-主路径", "查询待领取任务列表",
        "get", "/api/tasks", H_LIN, '{"status":"PENDING"}', None, None, None,
        "$..status", "PENDING", None, None,
        '{"PENDING_TASK_ID":"$.data[0].id"}', None, True,
    ),
    (
        3, "业务场景-制作人领取与制作提交", "场景1-主路径", "制作人领取待领取任务",
        "post", "/api/tasks/{{PENDING_TASK_ID}}/claim", H_LIN, None, None, None, None,
        "$..status", "IN_PROGRESS", None, None,
        '{"CLAIMED_TASK_ID":"$.data.id","ASSIGNEE_ID":"$.data.assigneeId"}', None, True,
    ),
    (
        4, "业务场景-制作人领取与制作提交", "场景1-主路径", "保存制作草稿",
        "patch", "/api/tasks/{{CLAIMED_TASK_ID}}/draft", H_LIN, None, None, DRAFT_OK, None,
        "$..status", "IN_PROGRESS", None, None, None, None, True,
    ),
    (
        5, "业务场景-制作人领取与制作提交", "场景1-主路径", "提交审核成功",
        "post", "/api/tasks/{{CLAIMED_TASK_ID}}/submit", H_LIN, None, None, SUBMIT_OK, None,
        "$..status", "IN_REVIEW", None, None, None, None, True,
    ),
    (
        6, "业务场景-制作人领取与制作提交", "场景1-主路径", "核对任务详情为待审核",
        "get", "/api/tasks/{{CLAIMED_TASK_ID}}", H_LIN, None, None, None, None,
        "$..status", "IN_REVIEW", None, None, None, None, True,
    ),
    # 场景1分支：驳回后再提（种子任务 task-006 / 陈默）
    (
        7, "业务场景-制作人领取与制作提交", "场景1-驳回后再提", "重置测试数据",
        "post", "/api/test/reset", None, None, None, None, None,
        "$..reset", True, None, None, None, None, True,
    ),
    (
        8, "业务场景-制作人领取与制作提交", "场景1-驳回后再提", "查看已驳回任务及驳回原因",
        "get", "/api/tasks/task-006", H_CHEN, None, None, None, None,
        "$..status", "REJECTED", None, None, None, None, True,
    ),
    (
        9, "业务场景-制作人领取与制作提交", "场景1-驳回后再提", "修改歌词音频并保存草稿",
        "patch", "/api/tasks/task-006/draft", H_CHEN, None, None, DRAFT_FIX, None,
        "$..status", "REJECTED", None, None, None, None, True,
    ),
    (
        10, "业务场景-制作人领取与制作提交", "场景1-驳回后再提", "驳回任务重新提交审核",
        "post", "/api/tasks/task-006/submit", H_CHEN, None, None, SUBMIT_FIX, None,
        "$..status", "IN_REVIEW", None, None, None, None, True,
    ),
    # 场景2：审核通过
    (
        11, "业务场景-审核流程", "场景2-审核通过", "重置测试数据",
        "post", "/api/test/reset", None, None, None, None, None,
        "$..reset", True, None, None, None, None, True,
    ),
    (
        12, "业务场景-审核流程", "场景2-审核通过", "审核员通过待审核任务",
        "post", "/api/tasks/task-004/review", H_ZHOU, None, None, REVIEW_APPROVE, None,
        "$..status", "APPROVED", None, None, None, None, True,
    ),
    (
        13, "业务场景-审核流程", "场景2-审核通过", "核对任务详情为已通过",
        "get", "/api/tasks/task-004", H_ZHOU, None, None, None, None,
        "$..status", "APPROVED", None, None, None, None, True,
    ),
    # 场景2：审核驳回
    (
        14, "业务场景-审核流程", "场景2-审核驳回", "重置测试数据",
        "post", "/api/test/reset", None, None, None, None, None,
        "$..reset", True, None, None, None, None, True,
    ),
    (
        15, "业务场景-审核流程", "场景2-审核驳回", "审核员填写原因驳回待审核任务",
        "post", "/api/tasks/task-004/review", H_ZHOU, None, None, REVIEW_REJECT, None,
        "$..status", "REJECTED", None, None, None, None, True,
    ),
    (
        16, "业务场景-审核流程", "场景2-审核驳回", "制作人核对驳回原因可查看",
        "get", "/api/tasks/task-004", H_LIN, None, None, None, None,
        "$..reviewReason", "歌词不完整请重写补充", None, None, None, None, True,
    ),
]


def main():
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    ws.append(headers_cn)
    ws.append(headers_en)
    for row in cases:
        ws.append(list(row))

    out = "data/mtm_api_cases.xlsx"
    wb.save(out)
    print(f"saved {out}, case steps={len(cases)}")


if __name__ == "__main__":
    main()
