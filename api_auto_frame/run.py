import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent
JSON_REPORT = ROOT / "report" / "test" / "json_report"
HTML_REPORT = ROOT / "report" / "test" / "html_report"


def run_cmd(args):
    """Windows 下 allure 是 .bat，需要 shell=True 才能找到。"""
    return subprocess.run(
        args,
        cwd=str(ROOT),
        shell=(sys.platform == "win32"),
        check=False,
    ).returncode


if __name__ == "__main__":
    exit_code = pytest.main([
        "-vs",
        str(ROOT / "testcases" / "test_runner.py"),
        "--alluredir",
        str(JSON_REPORT),
        "--clean-alluredir",
    ])

    allure = shutil.which("allure")
    if not allure:
        print("未找到 allure 命令，请确认 Allure 已安装并加入 PATH")
        print(f"原始结果目录: {JSON_REPORT}")
        sys.exit(exit_code or 1)

    # shell=True 时传字符串更稳妥
    gen_cmd = (
        f'"{allure}" generate "{JSON_REPORT}" -o "{HTML_REPORT}" --clean'
    )
    if run_cmd(gen_cmd) != 0:
        print("Allure 报告生成失败")
        sys.exit(1)

    print("正在打开 Allure 报告（关闭该窗口即停止报告服务）...")
    open_cmd = f'"{allure}" open "{HTML_REPORT}"'
    run_cmd(open_cmd)
    sys.exit(exit_code)
