import requests
import json
import time
import random
# 步骤
globalStep = 0
# 配置载入
with open("./config.json", "r") as f:
    config = json.load(f)

# 初始化
if config["init"] == 0:
    print("未配置, 首先请动手登录一次B站, 登录完成后请按回车继续\n")
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-logging')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    WebDriver = webdriver.Chrome(options=options)
    WebDriver.get("https://show.bilibili.com/platform/home.html")
    WebDriver.find_element(By.CLASS_NAME, "nav-header-register").click()
    input("登录完成后请按回车继续\n")
    config["cookie"] = WebDriver.get_cookies()
    WebDriver.quit()
    print("cookie已保存")
    config["url"] = input(
        "请输入购票链接并按回车继续, 格式例如 https://show.bilibili.com/platform/detail.html?id=72320\n"
    )
    config["project_id"] = int(config["url"][50:55])
    print("接下来输入场次和价格的横向顺序, 输入数字, 例如第一个场次和第一个价格即为 1 1\n")
    config["screennum"] = int(input("请输入场次顺序并按回车继续, 格式例如 1\n"))
    config["skunum"] = int(input("请输入价格顺序并按回车继续, 格式例如 1\n"))
    config["count"] = int(input("请输入购票数量并按回车继续, 购票人必须提前设置且设置的人数与你填的相符, 如 1\n"))
    config["process"] = int(input("请输入计划使用的进程数并按回车继续 如 1\n"))
    print("初始化成功\n")
    config["init"] = 1
    with open("./config.json", "w") as f:
        json.dump(config, f, indent=2)


# 状态
def status(response):
    global globalStep
    msg = response.json()
    if len(msg["msg"]) == 0:
        print("成功")
        globalStep += 1
        with open("./config.json", "w") as f:
            json.dump(config, f, indent=2)
    else:
        print("失败! Status Code" + " " + str(response.status_code) + " " +
              msg["msg"])
        print(response.json())


# 任务流
def flow():
    # 0 登录
    while globalStep < 7:
        time.sleep(random.uniform(0.3, 1))
        if globalStep == 0:
            # 1 获取信息
            # 获取 screen_id sku_id
            config["project_id"] = int(config["url"][50:55])
            print("1 获取信息")
            url = "https://show.bilibili.com/api/ticket/project/get?version=134&id=" + str(
                config["project_id"])
            response = requests.request("GET", url, headers=config["headers"])
            status(response)
            data = response.json()
            try:
                config["screen_id"] = int(
                    data["data"]["screen_list"][config["screennum"] - 1]["id"])
                config["sku_id"] = int(data["data"]["screen_list"][
                    config["screennum"] - 1]["ticket_list"][config["skunum"] -
                                                            1]["id"])
            except:
                continue

        elif globalStep == 1:
            # 2 Token获取
            # 需要 count project_id screen_id sku_id
            # 获取 token
            print("2 Token获取")
            url = "https://show.bilibili.com/api/ticket/order/prepare"
            payload = {
                "count": config["count"],
                "order_type": 1,
                "project_id": config["project_id"],
                "screen_id": config["screen_id"],
                "sku_id": config["sku_id"],
                "token": ""
            }
            response = requests.request("POST",
                                        url,
                                        headers=config["headers"],
                                        data=payload)
            status(response)
            try:
                data = response.json()
                config["token"] = data["data"]["token"]
            except:
                continue
        elif globalStep == 2:
            # 3 下单页信息
            # 需要 token
            # 获取 pay_money
            print("3 下单页信息")
            url = "https://show.bilibili.com/api/ticket/order/confirmInfo?token=" + config[
                "token"] + "&voucher="
            response = requests.request("GET", url, headers=config["headers"])
            status(response)
            try:
                data = response.json()
                config["pay_money"] = int(data["data"]["pay_money"])
            except:
                continue
        elif globalStep == 3:
            # 4 付款人
            # 需要 project_id
            # 获取 buyer
            print("4 付款人")
            url = "https://show.bilibili.com/api/ticket/buyer/list?is_default&projectId=" + str(
                config["project_id"])
            response = requests.request("GET", url, headers=config["headers"])
            status(response)
            try:
                data = response.json()
                for i in range(1, config["count"] + 1):
                    data["data"]["list"][i]["isBuyerInfoVerified"] = True
                    data["data"]["list"][i]["isBuyerValid"] = True
                config["buyer"] = data["data"]["list"]
            except:
                continue
        elif globalStep == 4:
            # 5 创建订单
            # 需要 buyer count pay_money project_id screen_id sku_id token
            # 获取 order_token
            print("5 创建订单")
            url = "https://show.bilibili.com/api/ticket/order/createV2"
            payload = {
                "buyer_info": config["buyer"],
                "count": config["count"],
                "deviceId": "4aac6f1261084849aeef4d26bb79c59e",
                "order_type": 1,
                "pay_money": config["pay_money"],
                "project_id": config["project_id"],
                "screen_id": config["screen_id"],
                "sku_id": config["sku_id"],
                "timestamp": int(round(time.time() * 1000)),
                "token": config["token"]
            }
            response = requests.request("POST",
                                        url,
                                        headers=config["headers"],
                                        data=payload)
            status(response)
            try:
                data = response.json()
                config["order_token"] = data["data"]["token"]
            except:
                continue
        elif globalStep == 5:
            # 6 支付信息
            # 需要 order_token
            # 获取 order_id
            print("6 支付信息")
            url = "https://show.bilibili.com/api/ticket/order/createstatus?token=" + config[
                "order_token"] + "&timestamp=" + str(
                    int(round(time.time() * 1000)))
            response = requests.request("GET", url, headers=config["headers"])
            status(response)
            try:
                data = response.json()
                config["order_id"] = data["data"]["order_id"]
            except:
                continue
        elif globalStep == 6:
            # 7 订单状态
            # 需要 order_id
            print("7 订单状态")
            url = "https://show.bilibili.com/api/ticket/order/info?order_id=" + config[
                "order_id"] + "&timestamp=" + str(
                    int(round(time.time() * 1000)))
            response = requests.request("GET", url, headers=config["headers"])
            status(response)
            try:
                data = response.json()
                if data["data"]["status_name"] == "待支付":
                    exit()
            except:
                continue


# 线程
if config["process"] == 1:
    print("单线程模式")
    flow()
else:
    print("多线程模式")
    process_list = []
    exec("from multiprocessing import Process")
    for i in range(1, config["process"] + 1):
        exec("p%d = Process(target=flow)" % i)
    if __name__ == "__main__":
        for i in range(1, config["process"] + 1):
            exec("p%d.start() " % (i))
            exec("process_list.append(p%d) " % (i))
        for t in process_list:
            t.join()
