from selenium.webdriver.common.by import By
from selenium import webdriver
import json
import random
import time
from multiprocessing import Process

option = webdriver.ChromeOptions()
# 配置载入
with open('./config.json', 'r') as f:
    config = json.load(f)

# Cookie初始化
if len(config["cookie"]) == 0:
    print("cookies未设置,请手动登录一次")
    WebDriver = webdriver.Chrome()
    WebDriver.get(config["studyUrl"])
    time.sleep(random.uniform(0.1, 0.6))
    WebDriver.find_element(By.CLASS_NAME, "nav-header-register").click()
    input("登录完成后请按任意键继续\n")
    config["cookie"] = WebDriver.get_cookies()
    with open('./config.json', 'w') as f:
        json.dump(config, f, indent=4)
    print("cookie已保存")
    WebDriver.quit()
else:
    prefs = {"profile.managed_default_content_settings.images": 2}    # 设置无图模式
    option.add_experimental_option("prefs", prefs)    # 加载无图模式设置
    if config["noWindows"] == 1:
        option.add_argument('--headless')
        option.add_argument('--no-sandbox')


def order():
    # WebDriver初始化
    WebDriver = webdriver.Chrome(chrome_options=option)
    WebDriver.get(config["studyUrl"])

    # 载入Cookie
    for cookie in config["cookie"]:
        WebDriver.add_cookie({
            'domain': cookie['domain'],
            'name': cookie['name'],
            'value': cookie['value'],
            'path': cookie['path']
        })

    # 时间戳获取
    if len(config["currentToken"]) == 0:
        print("获取时间戳中")
        WebDriver.get(config["studyUrl"])
        WebDriver.find_element(By.CLASS_NAME, "product-buy.enable").click()
        time.sleep(random.uniform(0.1, 0.6))
        config["currentToken"] = WebDriver.current_url[59:65]
        config["actualUrl"] = "https://show.bilibili.com/platform/confirmOrder.html?token=" + \
            config["currentToken"] + config["afterToken"]
        with open('./config.json', 'w') as f:
            json.dump(config, f, indent=4)

    # 下单页面
    config["actualUrl"] = "https://show.bilibili.com/platform/confirmOrder.html?token=" + \
        config["currentToken"] + config["afterToken"]
    WebDriver.get(config["actualUrl"])
    with open('./config.json', 'w') as f:
        json.dump(config, f, indent=4)

    # 持续下单
    while True:
        time.sleep(random.uniform(0.6, 1))
        try:
            try:
                # 时间戳失效
                if WebDriver.find_element(
                        By.XPATH,
                        "//*[@id='app']/div[2]/div/div[5]/div/div[2]/div/div[2]/div"
                ).text == "当前页面已失效，请返回详情页重新下单":
                    print("时间戳已过期,获取时间戳中")
                    WebDriver.get(config["studyUrl"])
                    WebDriver.find_element(By.CLASS_NAME,
                                           "product-buy.enable").click()
                    time.sleep(random.uniform(0.1, 0.6))
                    config["currentToken"] = WebDriver.current_url[59:65]
                    config["actualUrl"] = "https://show.bilibili.com/platform/confirmOrder.html?token=" + \
                        config["currentToken"] + config["afterToken"]
                    WebDriver.get(config["actualUrl"])
                    with open('./config.json', 'w') as f:
                        json.dump(config, f, indent=4)
                    time.sleep(3)
            except BaseException:
                WebDriver.find_element(By.CLASS_NAME,
                                       "confirm-paybtn.active").click()
                print("运行中")
        except Exception as e:
            try:
                if WebDriver.find_element(
                        By.XPATH, "//*[@id='app']/div[2]/div/div[7]/div/h1"
                ).text == "扫码支付":
                    print("已下单,请手动支付")
                    WebDriver.quit()
                    exit(0)
            except BaseException:
                print(e)
                WebDriver.find_element(By.CLASS_NAME, "check-icon").click()
                print("无法创建订单")
                WebDriver.refresh()


# 多线程
if config["multi"] == 0:
    print("单线程模式")
    order()
else:
    print("多线程模式")
    process_list = []
    p1 = Process(target=order)
    p2 = Process(target=order)
    p3 = Process(target=order)
    p4 = Process(target=order)
    if __name__ == '__main__':
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        process_list.append(p1)
        process_list.append(p2)
        process_list.append(p3)
        process_list.append(p4)
        for t in process_list:
            t.join()
