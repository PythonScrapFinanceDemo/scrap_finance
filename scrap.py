from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')

url = "http://spds.qhrb.com.cn/SP10/SPOverSee1.aspx"

driver = webdriver.Chrome("/usr/local/chromedriver-Linux64")
#driver = webdriver.Chrome("/usr/bin/google-chrome")
driver.get(url)

#html = urlopen("http://spds.qhrb.com.cn/SP10/SPOverSee1.aspx")

bsObj = BeautifulSoup(driver.page_source,'html.parser')


#计算总页数
page_option = bsObj.find('select',id="AspNetPager1_input").findAll('option')
page_length = int(page_option[len(page_option)-1].get_text())    #获得所有页数

def get_plain_text(ResultSet):
    text = []
    for i in ResultSet:
        text.append(i.get_text())
    return text

columns = bsObj.findAll(style="padding-top: 1px;")
columns_text = get_plain_text(columns)



user_information_obj = bsObj.findAll('tr',style="background: #fff;")
user_length = len(user_information_obj)
user_rank = []
user_name = []
user_interest = []
user_risk_degree = []
user_net_profit = []
user_net_profit_score = []
user_retreat_rates = []
user_retreat_rates_score = []
user_net_day = []
user_total_net_worth = []
user_net_score = []
user_total_score = []
user_reference_yields = []
user_dealer = []
user_operate_guide = []
user_account_evaluation = []
user_information = [user_rank,user_name,user_interest,user_risk_degree,
                    user_net_profit,user_net_profit_score,user_retreat_rates,user_retreat_rates_score,
                    user_net_day,user_total_net_worth,user_net_score,user_total_score,
                    user_reference_yields,user_dealer,
                    user_operate_guide,user_account_evaluation]

for user_i in user_information_obj:
    for i,td_i in enumerate(user_i.findAll("td")):
        user_information[i].append(td_i.get_text())

#print(page_length) test

# 获取下一页的按钮，每页12个，下一页是第11个按钮,然后点击
page = 1
def next_page(page):
    next_page_button = driver.find_elements_by_xpath("//a[@class='Pager']")[10]
    next_page_button.click()

    page_now = int(bsObj.find('select',id="AspNetPager1_input").find('option',selected="true").get_text())
    logging.debug('Now page is:%s', page_now)
    page = page + 1

next_page(page)
next_page(page)
next_page(page)
#
'''
test
driver.find_elements_by_xpath("//a[@class='Pager']")[10].click()
page = page + 1
driver.find_elements_by_xpath("//a[@class='Pager']")[10].click()
page = page + 1
next_page(page)
next_page(page)
next_page(page)
'''

logging.debug('End of program')
