import logging
import os
import time
import allure

from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.keywords_utils import kw_step
# 用 Select 类来处理下拉框, 需要先导包
from selenium.webdriver.support.select import Select


class Keywords:
    def __init__(self, driver):
        self.driver = driver

    # 等待查找，最多等10秒，默认10秒内没找到元素则报错
    def find(self, step, clickable=False):
        """查找元素"""
        wait = WebDriverWait(self.driver, 10)
        locator = step['by'], step['value']
        try:
            # 如果索引为 None 则定位单个元素，反之则定位一组元素中指定索引的元素
            if step["index"] is None:
                condition = EC.element_to_be_clickable(locator) if clickable else EC.presence_of_element_located(locator)
                return wait.until(condition)
            else:
                return wait.until(EC.presence_of_all_elements_located(locator))[step['index']]
        except TimeoutException:
            logging.info(f"❌元素定位失败，元素定位信息为：{locator}")

    def _retry_action(self, step, action, clickable=False, retries=3):
        """页面重渲染时元素可能失效，失败后重新定位再试"""
        last_error = None
        for _ in range(retries):
            try:
                element = self.find(step, clickable=clickable)
                return action(element)
            except StaleElementReferenceException as e:
                last_error = e
                time.sleep(0.3)
        raise last_error

    # 核心操作关键字
    @kw_step   # 自定义装饰器：用来添加allure报告和日志中的步骤信息
    def open(self, step):
        """打开网址"""
        self.driver.get(step['data'])

    @kw_step
    def click(self, step):
        """点击元素"""
        self._retry_action(step, lambda el: el.click(), clickable=True)

    @kw_step
    def input(self, step):
        """输入文本"""
        self._retry_action(step, lambda el: el.send_keys(step['data']), clickable=True)

    @kw_step
    def clear(self, step):
        """清空文本"""
        self._retry_action(step, lambda el: el.clear(), clickable=True)

    @kw_step
    def wait(self, step):
        """等待"""
        time.sleep(step['data'])

    @kw_step
    def shot(self, step):
        """截图：先等页面加载完成，再稍作停留后截图，避免截到空白/半加载页"""
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        # data 可配置额外等待秒数，未配置时默认等 1.5 秒让接口/渲染完成
        extra_wait = step.get("data")
        time.sleep(float(extra_wait) if extra_wait not in (None, "") else 1.5)
        now_time = time.strftime("%Y-%m-%d %H_%M_%S")
        png = self.driver.get_screenshot_as_png()
        allure.attach(
            png,
            f"第{step['step_num']}步_{now_time}.png",
            allure.attachment_type.PNG
        )

    @kw_step
    def refresh(self, step):
        """刷新页面"""
        self.driver.refresh()

    @kw_step
    def forword(self, step):
        """前进"""
        self.driver.forward()

    @kw_step
    def back(self, step):
        """后退"""
        self.driver.back()

    @kw_step
    def swich_to_window(self, step):
        """切换窗口"""
        headles = self.driver.window_handles    # 获取所有窗口的句柄
        self.driver.switch_to.window(headles[step['data']])    # 切换到指定窗口，data中存放索引数据，-1表示最新窗口

    # 下拉框操作：通过文本选择、通过值选择
    @kw_step
    def select_by_text(self, step):
        """通过文本选择"""
        select = Select(self.find(step))
        select.select_by_visible_text(step['data'])

    @kw_step
    def select_by_value(self, step):
        """通过value选择"""
        select = Select(self.find(step))
        select.select_by_value(step['data'])

    # 弹出框操作：点击确定、点击取消
    @kw_step
    def alert_accept(self, step):
        """弹出框点击确定"""
        self.driver.switch_to.alert.accept()

    @kw_step
    def alert_dismiss(self, step):
        """弹出框点击取消"""
        self.driver.switch_to.alert.dismiss()

    # 滚动条操作：滚动 和 js 执行操作
    @kw_step
    def scroll(self, step):
        """
        滚动到某个绝对坐标的位置
        step['data']数据要写成{‘x’:100,‘y’:100}
        """
        # 这里eval（）可以将字符串转化成字典
        position_dict = eval(step['data'])
        # 定义js脚本，绝对坐标的格式转换成 -> (x,y)
        js = f"window.scrollTo({position_dict['x']},{position_dict['y']})"
        self.driver.execute_script(js)

    @kw_step
    def js_execute(self, step):
        """
        执行js脚本
        """
        self.driver.execute_script(step['data'])

    # 键鼠常用交互: 双击, 右击, 悬停, 拖拽, 回车
    @kw_step
    def double_click(self, step):
        """双击"""
        element = self.find(step)
        action = ActionChains(self.driver)
        action.double_click(element).perform()

    @kw_step
    def right_click(self, step):
        """右击"""
        element = self.find(step)
        action = ActionChains(self.driver)
        action.context_click(element).perform()

    @kw_step
    def hover(self, step):
        """悬停"""
        element = self.find(step)
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()

    @kw_step
    def drag_and_drop(self, step):
        """
        拖拽
        step['data'] 数据要写成 {'by': 'xpath', 'value': 'xxx'} 的形式
        """
        source = self.find(step)
        # 目标元素数据需要处理
        target_dict = eval(step["data"])
        target = self.driver.find_element(target_dict["by"], target_dict["value"])
        action = ActionChains(self.driver)
        action.drag_and_drop(source, target).perform()

    @kw_step
    def enter(self, step):
        """回车"""
        element = self.find(step)
        element.send_keys(Keys.ENTER)

    # 文件上传
    @kw_step
    def upload(self, step):
        """上传文件"""
        # 相对路径转化为绝对路径
        relative_path = step['data']
        absolute_path = os.path.abspath(relative_path)

        element = self.find(step)
        element.send_keys(absolute_path)

    # frame操作: 切换到某个frame, 切回主文档
    @kw_step
    def switch_to_frame(self, step):
        """根据frame元素把焦点切换到某个frame"""
        element = self.find(step)
        self.driver.switch_to.frame(element)

    @kw_step
    def switch_to_default_content(self, step):
        """从frame切回到主文档"""
        self.driver.switch_to.default_content()