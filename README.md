# 音乐任务管理平台 — 测试提交包

本仓库一次包含文档 + UI 自动化 + 接口自动化，方便统一提交。

> **说明：** 不能直接打开 CMD 就跑。需先配置 Python / 依赖 / 浏览器驱动 / Allure，并启动被测服务后，再执行 `python run.py`。

## 目录结构

```
mango_lantern_qa/
├── README.md                 # 本说明
├── docs/                     # 测试计划、Bug 整理、自动化框架测试结果等文档
├── ui_auto_frame/            # UI 自动化框架与用例
└── api_auto_frame/           # 接口自动化框架与用例
```

| 目录 | 内容 | 详细说明 |
|------|------|----------|
| `docs/` | 测试计划、缺陷/Bug 整理等 | 直接打开文档查看 |
| `ui_auto_frame/` | Selenium + Excel 关键字驱动 | `ui_auto_frame/使用说明.md` |
| `api_auto_frame/` | Requests + Excel 数据驱动 | `api_auto_frame/使用说明.md` |

---

## 一、环境要求（运行前必做）

### 1. 公共环境

| 项 | 说明 |
|----|------|
| 操作系统 | Windows 即可 |
| Python | 建议 3.10+，命令行能执行 `python` / `pip` |
| Allure | 已安装并加入 PATH（`allure --version` 有输出） |
| 被测服务 | UI 前端、接口服务需先启动 |

### 2. UI 额外要求

| 项 | 说明 |
|----|------|
| 浏览器 | Chrome 或 Edge |
| 浏览器驱动 | `chromedriver.exe` / `msedgedriver.exe` 放到 `ui_auto_frame/driver/`，版本需与浏览器匹配 |
| 前端地址 | 默认用例访问 `http://localhost:5173/tasks` |

### 3. 接口额外要求

| 项 | 说明 |
|----|------|
| 接口地址 | 默认 `http://localhost:3000`（见 `api_auto_frame/config/config.py`） |

---

## 二、安装依赖

在项目根目录打开 CMD / PowerShell：

```bash
# 接口自动化
cd api_auto_frame
pip install -r requirements.txt

# UI 自动化
cd ../ui_auto_frame
pip install -r requirements.txt
```

---

## 三、修改配置

### UI：`ui_auto_frame/config/config.py`

- `BROWSER_TYPE`：`chrome` / `edge`
- `EXCEL_FILE`：用例文件路径（默认已指向音乐任务关键字用例）
- 用例中的打开地址如与本机不符，需在 Excel 中同步修改

### 接口：`api_auto_frame/config/config.py`

- `BASE_URL`：接口基地址，默认 `http://localhost:3000`
- `EXCEL_FILE`：用例文件路径

---

## 四、启动被测服务后再跑

1. 启动前端（示例：`http://localhost:5173`）
2. 启动接口服务（示例：`http://localhost:3000`）
3. 确认浏览器能手动打开页面、接口可访问

然后执行：

```bash
# UI
cd ui_auto_frame
python run.py

# 接口
cd api_auto_frame
python run.py
```

执行后会：跑用例 → 生成 Allure 报告 → 自动打开报告页面。  
关闭报告服务窗口（或 Ctrl+C）即可结束。

---

## 五、常见问题

| 现象 | 处理 |
|------|------|
| `python` / `pip` 不是内部命令 | 安装 Python，并勾选加入 PATH |
| `allure` 不是内部命令 | 安装 Allure 并配置环境变量 |
| UI 启动浏览器失败 | 检查驱动版本是否匹配，驱动是否在 `driver/` |
| 打开页面超时 / 接口连不上 | 先确认被测服务已启动，地址与 config 一致 |
| 找不到模块（ModuleNotFoundError） | 回到对应目录重新 `pip install -r requirements.txt` |

---

