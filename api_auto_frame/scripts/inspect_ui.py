import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def dump(driver, title):
    print(f"\n===== {title} =====")
    print("url:", driver.current_url)
    print("--- body ---")
    print(driver.find_element(By.TAG_NAME, "body").text[:3000])
    print("--- buttons ---")
    for e in driver.find_elements(By.TAG_NAME, "button"):
        print(" btn:", repr(e.text.strip()), "disabled=", e.get_attribute("disabled"))
    print("--- links ---")
    for e in driver.find_elements(By.TAG_NAME, "a"):
        txt = e.text.strip().replace("\n", " ")
        if txt:
            print(" a:", repr(txt), "href=", e.get_attribute("href"))
    print("--- fields ---")
    for e in driver.find_elements(By.CSS_SELECTOR, "input,textarea"):
        print(
            " field:",
            e.tag_name,
            "ph=",
            repr(e.get_attribute("placeholder")),
            "aria=",
            repr(e.get_attribute("aria-label")),
            "type=",
            e.get_attribute("type"),
        )


def main():
    requests.post("http://localhost:3000/api/test/reset", timeout=10)

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1400,900")
    driver = webdriver.Chrome(options=opts)
    try:
        driver.get("http://localhost:5173/tasks")
        time.sleep(1.5)
        dump(driver, "列表页")

        driver.find_element(By.XPATH, "//button[contains(.,'重置数据')]").click()
        time.sleep(1.2)

        driver.find_element(By.XPATH, "//a[contains(.,'海岸线')]").click()
        time.sleep(1.5)
        dump(driver, "待领取详情-海岸线")

        # 尝试领取
        buttons = driver.find_elements(By.TAG_NAME, "button")
        claim = [b for b in buttons if "领取" in b.text]
        if claim:
            claim[0].click()
            time.sleep(1.2)
            dump(driver, "领取后详情")

            # 填写并提交
            areas = driver.find_elements(By.TAG_NAME, "textarea")
            inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text'],input:not([type])")
            print("textarea count", len(areas), "text inputs", len(inputs))
            if areas:
                areas[0].clear()
                areas[0].send_keys("这是一首关于海岸线的歌，海风吹过沙滩留下脚印与回声。")
            for inp in driver.find_elements(By.CSS_SELECTOR, "input"):
                ph = (inp.get_attribute("placeholder") or "") + (inp.get_attribute("aria-label") or "")
                if "音频" in ph or "http" in ph.lower() or "audio" in ph.lower() or "地址" in ph:
                    inp.clear()
                    inp.send_keys("https://audio.example.com/demo.mp3")
                    break
            else:
                # 兜底：第二个可见文本框
                text_inputs = [
                    i
                    for i in driver.find_elements(By.CSS_SELECTOR, "input")
                    if i.is_displayed() and (i.get_attribute("type") in (None, "", "text", "url"))
                ]
                if text_inputs:
                    text_inputs[-1].clear()
                    text_inputs[-1].send_keys("https://audio.example.com/demo.mp3")

            submit = [b for b in driver.find_elements(By.TAG_NAME, "button") if "提交" in b.text]
            print("submit buttons:", [b.text for b in submit])
            if submit:
                submit[0].click()
                time.sleep(1.5)
                dump(driver, "提交后")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
