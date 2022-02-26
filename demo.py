from selenium import webdriver
from selenium.webdriver.common import alert
from selenium.webdriver.support.ui import Select
import time

course_name = "X86汇编程序设计"
log_name = course_name + ".log"


def log(context):
    print(time.asctime(time.localtime(time.time())) + "\t" + context)


def login():
    global browser
    # 登录vpn
    login_url = "https://e1.buaa.edu.cn/users/sign_in"
    browser.get(login_url)
    user_name = browser.find_element_by_id("user_login")
    password = browser.find_element_by_id("user_password")
    submit_button = browser.find_element_by_name("commit")
    user_name.send_keys("***********************")
    password.send_keys("*******************************")
    submit_button.click()

    jiaowu_url = "https://10-200-21-61-7001.e1.buaa.edu.cn/ieas2.1/welcome"
    browser.get(jiaowu_url)
    if browser.title == "统一身份认证网关":
        buaa_sso()
        browser.get(jiaowu_url)


def genXpath(index):
    button = '/html/body/div[7]/div/div[6]/table/tbody/tr[' + str(index) + ']/td[1]/div/a/span'
    name = '/html/body/div[7]/div/div[6]/table/tbody/tr[' + str(index) + ']/td[4]/a'
    return (button, name)


def buaa_sso():
    global browser
    user_name = browser.find_element_by_id("username")
    password = browser.find_element_by_id("password")
    submit_button = browser.find_element_by_xpath('//*[@id="fm1"]/div[3]/input[4]')
    user_name.send_keys("************************")
    password.send_keys("******************************")
    submit_button.click()


def run():
    global browser

    # 打开选课界面
    zhuanyeke_url = "https://10-200-21-61-7001.e1.buaa.edu.cn/ieas2.1/xslbxk/queryXsxk?pageXkmkdm=ZYL"
    browser.get(zhuanyeke_url)

    # 填写院系表单
    faculty = Select(browser.find_element_by_id("pageKkyxid"))
    faculty.select_by_value("06")
    # 选一般专业课类
    browser.find_element_by_xpath('/html/body/div[7]/div/div[3]/table/tbody/tr/td[1]/ul/li[2]/a').click()
    # 点击查询按钮
    query_button = browser.find_element_by_xpath('//*[@id="queryform"]/ul/li[6]/div/a/span')
    query_button.click()

    # 寻找指定的课程名
    try:
        for i in range(2, 11):
            (button_xpath, name_xpath) = genXpath(i)
            name_element = browser.find_element_by_xpath(name_xpath)
            if name_element.text == course_name:
                button_element = browser.find_element_by_xpath(button_xpath)
                button_element.click()
                log(alert.text)
                alert.accept()
                break
        else:
            log("no such class")
    except:
        log("no such class")


# 主程序
log("start")
while True:
    # 启动浏览器
    option = webdriver.ChromeOptions()
    # option.add_argument('--headless')
    # option.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=option)
    try:
        login()
        while True:
            run()
    except Exception as e:
        log(str(e))
        log("发生错误 重启脚本")
        browser.quit()
        pass