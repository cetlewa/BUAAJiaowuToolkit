import sys
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common import alert

userId = "******"
userPwd = "******"
cosId = "******"


# F-核心通识 G-一般通识 I-核心专业 J-一般专业
cosSch = "01"
cosSec = "/html/body/div[2]/div[2]/div/div[6]/div/a[4]/span[2]"
cosTrd = "/html/body/div[7]/div/div[3]/table/tbody/tr/td[1]/ul/li[2]/a"

jwxt_sso = "https://sso.buaa.edu.cn/login?service=http%3A%2F%2Fjwxt.buaa.edu.cn%3A8080%2Fieas2.1%2Fwelcome%3Ffalg%3D1"

logName = cosId + ".log"


def log(context):
    print(time.asctime(time.localtime(time.time()))+"\t"+context)

def get_cos_type():
    global cosSch, cosSec, cosTrd
    cosSch = cosId[3:5]
    if cosId[2:3] == "F":
        cosSec = "通识课程选课"
        cosTrd = "核心通识类"
    elif cosId[2:3] == "G":
        cosSec = "通识课程选课"
        cosTrd = "一般通识类"
    elif cosId[2:3] == "I":
        cosSec = "专业课程选课"
        cosTrd = "核心专业类"
    elif cosId[2:3] == "J":
        cosSec = "专业课程选课"
        cosTrd = "一般专业类"

def login():
    global browser
    # open sso login page
    browser.get(jwxt_sso)
    # locate and switch to ifram
    ifram = browser.find_element_by_xpath("/html/body/iframe")
    browser.switch_to.frame(ifram)
    # locate userId and userPwd box and input
    user_id = browser.find_element_by_xpath("/html/body/div[2]/div/div[3]/div[2]/div[1]/div[1]/div/input")
    user_pwd = browser.find_element_by_xpath("/html/body/div[2]/div/div[3]/div[2]/div[1]/div[3]/div/input")
    user_id.send_keys(userId)
    user_pwd.send_keys(userPwd)
    # locate and click submit button
    submit_button = browser.find_element_by_xpath("/html/body/div[2]/div/div[3]/div[2]/div[1]/div[7]/input")
    submit_button.click()
    time.sleep(0.5)

def open_cos_page():
    global browser
    # open select page
    browser.find_element_by_link_text("学生选课").click()
    # wait for animation
    time.sleep(0.5)
    # click second menu
    browser.find_element_by_link_text(cosSec).click()
    # locate and switch to iframe
    iframe = browser.find_element_by_xpath("/html/body/div[4]/div[1]/iframe")
    browser.switch_to.frame(iframe)
    # click third menu
    browser.find_element_by_link_text(cosTrd).click()
    # insert information
    insert_info()
    # click search
    browser.find_element_by_class_name("addlist_button2.mt4").click()
    # time.sleep(0.5)

def genXpath(index):
    button_xpath = "/html/body/div[7]/div/div[6]/table/tbody/tr[" + str(index) + "]/td[1]/div/a/span"
    id_xpath = "/html/body/div[7]/div/div[6]/table/tbody/tr[" + str(index) + "]/td[3]"
    name_xpath = "/html/body/div[7]/div/div[6]/table/tbody/tr[" + str(index) + "]/td[4]/a"
    return (button_xpath, id_xpath, name_xpath)

def insert_info():
    # select cos school
    school = browser.find_element_by_name("pageKkyx")
    s = Select(school)
    s.select_by_value(cosSch)
    # hide conflict
    conflict = browser.find_element_by_name("pageYcctkc")
    if not conflict.is_selected():
        conflict.click()

def locate_cos():
    try:
        for i in range(2, 20):
            (button_xpath, id_xpath, name_xpath) = genXpath(i)
            id_element = browser.find_element_by_xpath(id_xpath)
            if id_element.text == cosId:
                return (button_xpath, id_xpath, name_xpath)
        else:
            log("no such class")
    except:
        log("no such class")


# main
log("start")
while True:
    # open browser
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=option)
    try:
        get_cos_type()
        login()
        open_cos_page()
        (button_xpath, id_xpath, name_xpath) = locate_cos()
        while True:
            insert_info()
            # click search
            browser.find_element_by_class_name("addlist_button2.mt4").click()
            # click select
            browser.find_element_by_xpath(button_xpath).click()
            # accept alert
            alert = browser.switch_to.alert
            log(alert.text)
            if alert.text == "选课成功":
                sys.exit(0)
            alert.accept()
            # time.sleep(1)
    except Exception as e:
        log(str(e))
        log("something wrong, reboot programme")
        browser.quit()
        pass
