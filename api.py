# -*- coding: UTF-8 -*-
import json
import os
import time
from shutil import copyfile

import requests
from requests.exceptions import Timeout

with open("./config.json", "r") as f:
    config = json.load(f)

session = requests.session()


# 初始化
def initConfig():
    print("让我们配置一下脚本, 请跟随提示进行操作, 如果操作失误可按Ctrl+C退出, 然后重新进入\n")
    print("首先请动手登录一次B站, 登录完成后请按回车继续\n")
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
    config["bid"] = int(input("请输入该账户的UID 如10000\n"))
    config["url"] = input(
        "请输入购票链接并按回车继续, 格式例如 https://show.bilibili.com/platform/detail.html?id=72320\n"
    )
    config["projectId"] = int(config["url"][50:55])
    print("接下来输入场次和价格的横向顺序, 输入数字, 例如第一个场次和第一个价格即为 1 1\n")
    config["screennum"] = int(input("请输入场次顺序并按回车继续, 格式例如 1\n"))
    config["skunum"] = int(input("请输入价格顺序并按回车继续, 格式例如 1\n"))
    config["count"] = int(input("请输入购票数量并按回车继续, 购票人必须提前设置且设置的人数与你填的相符, 如 1\n"))
    config["timeout"] = int(input("请输入请求超时时间并按回车继续 如 1\n"))
    config["process"] = int(input("请输入计划使用的进程数并按回车继续 如 1\n"))
    print("初始化成功\n")
    config["init"] = 1
    with open("./config.json", "w") as f:
        json.dump(config, f, indent=2)


# 配置载入
if os.path.exists("./config.json"):
    with open("./config.json", "r") as f:
        config = json.load(f)
    if config["init"] == 0:
        initConfig()
else:
    copyfile("./config_example.json", "./config.json")
    with open("./config.json", "r") as f:
        config = json.load(f)
    initConfig()


def orderInfo():
    # 获取订单信息
    url = "https://show.bilibili.com/api/ticket/project/get?version=134&id=71931&project_id=71931"

    headers = {
        'sec-ch-ua':
        '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty'
    }
    session.headers.update(headers)
    response = session.request("GET",
                               url,
                               headers=headers,
                               timeout=config["timeout"])

    data = response.json()
    config["screen_id"] = int(data["data"]["screen_list"][config["screennum"] -
                                                          1]["id"])
    config["sku_id"] = int(
        data["data"]["screen_list"][config["screennum"] -
                                    1]["ticket_list"][config["skunum"] -
                                                      1]["id"])
    config["pay_money"] = int(data["data"]["screen_list"][config["screen_id"]]
                              ["ticket_list"][config["sku_id"]]["price"])

    # 获取购票人
    url = "https://show.bilibili.com/api/ticket/buyer/list?is_default&projectId=71931"

    headers = {
        'sec-ch-ua':
        '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty'
    }

    response = session.request("GET",
                               url,
                               headers=headers,
                               timeout=config["timeout"])
    data = response.json()

    for i in range(0, config["count"]):
        data["data"]["list"][i]["isBuyerInfoVerified"] = True
        data["data"]["list"][i]["isBuyerValid"] = True
        config["buyerList"] = data["data"]["list"]


def token():
    # 获取token
    url = "https://show.bilibili.com/api/ticket/order/prepare?project_id=71931"

    payload = 'count=1&order_type=1&project_id=71931&screen_id=124017&sku_id=377420&token='

    headers = {
        'sec-ch-ua':
        '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-platform': '"Windows"',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty'
    }

    response = session.request("POST",
                               url,
                               headers=headers,
                               data=payload,
                               timeout=config["timeout"])
    data = response.json()
    config["token"] = data["data"]["token"]


def orderCreate():
    # 创建订单
    url = "https://show.bilibili.com/api/ticket/order/createV2?project_id=71931"

    payload = {
        "buyer_info": config["buyer"],
        "count": config["count"],
        "deviceId": "",
        "order_type": 1,
        "pay_money": config["pay_money"] * config["count"],
        "project_id": config["project_id"],
        "screen_id": config["screen_id"],
        "sku_id": config["sku_id"],
        "timestamp": int(round(time.time() * 1000)),
        "token": config["token"]
    }

    headers = {
        'x-risk-header': 'platform/pc uid/' + config["bid"] +
        ' deviceId/C4B85792-D2E6-44FD-83EE-A23CF2839DA0167634infoc',
        'sec-ch-ua':
        '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'Content-Type': 'application/x-www-form-urlencoded',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty'
    }

    response = session.request("POST",
                               url,
                               headers=headers,
                               data=payload,
                               timeout=config["timeout"])
    data = response.json()
    if data["errno"] == 0:
        print("已成功抢到票, 请尽快支付 https://show.bilibili.com/orderlist")
        exit(0)


def flow():
    session.get("https://show.bilibili.com/platform/home.html")
    cookie = requests.cookies.RequestsCookieJar()    # type: ignore
    for i in config["cookie"]:
        cookie.set(domain=i["domain"],
                   name=i["name"],
                   value=i["value"],
                   path=i["path"])
    session.cookies.update(cookie)


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
