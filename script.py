import requests, json, random, time

# 配置载入
with open('./config.json', 'r') as f:
    config = json.load(f)

# Cookie初始化
if len(config["cookie"]) == 0:
    print("cookies未设置,请手动登录一次")
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    WebDriver = webdriver.Chrome()
    WebDriver.get("https://show.bilibili.com/platform/home.html")
    WebDriver.find_element(By.CLASS_NAME, "nav-header-register").click()
    input("登录完成后请按任意键继续\n")
    config["cookie"] = WebDriver.get_cookies()
    WebDriver.quit()
    with open('./config.json', 'w') as f:
        json.dump(config, f, indent=4)
    print("cookie已保存")


# 任务流
def flow():
    print("test")


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
    if __name__ == '__main__':
        for i in range(1, config["process"] + 1):
            exec("p%d.start() " % (i))
            exec("process_list.append(p%d) " % (i))
        for t in process_list:
            t.join()
