import logging

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from core.keywords import Keywords
from utils.keywords_utils import kw_step
from selenium.webdriver.support import expected_conditions as EC


class BusinessKeywords(Keywords):
    # 重写一个适合业务关键字的定位元素的方法

    def locate(self, by, value):
        """查找元素"""
        wait = WebDriverWait(self.driver, 10)
        locator = by, value
        try:
            return wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            logging.info(f"❌元素定位失败，元素定位信息为: {locator}")

    # 为具体一个项目的功能实现单独开发的关键字
    @kw_step
    def login(self, step):
        """
        封装登录操作
        step['data'], 需要做特殊处理, 数据要写为 {'username': 'xx', 'password': 'xx', 'code': 'xx'}
        """
        self.driver.get("http://192.168.10.130/")
        # 数据处理
        login_data = eval(step['data'])
        # 业务过程
        self.locate("xpath", "//input[@placeholder='账号']").send_keys(login_data['username'])
        self.locate("xpath", "//input[@placeholder='密码']").send_keys(login_data['password'])
        self.locate("xpath", "//input[@placeholder='验证码']").send_keys(login_data['code'])
        self.locate("xpath", "//button[.='登 录']").click()

    @kw_step
    def get_attribute(self, step):
        """
        获取元素属性，常用于获取动态元素的某个属性，以便后续其他元素的定位
        step['data'] 写成 {'A': '保存到全局变量中的变量名(key)': '提取这个属性名'} 形式
        # 在只有一组键值对的情况下，可以用下面这个方法提取第一个键值对的 key 和 value
        """
        key, attribute_name = next(iter(eval(step['data']).items()))
        attribute_value = self.find(step).get_attribute(attribute_name)
        return key, attribute_value