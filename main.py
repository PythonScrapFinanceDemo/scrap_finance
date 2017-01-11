from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import logging
import pandas as pd
import numpy as np

import package_scrap.scrap as scrap
import package_scrap.date as dt

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')

url = "http://spds.qhrb.com.cn/SP10/SPOverSee1.aspx"

#driver = webdriver.Chrome("/usr/local/chromedriver-Linux64")
driver = webdriver.PhantomJS()
driver.get(url)

#html = urlopen("http://spds.qhrb.com.cn/SP10/SPOverSee1.aspx")

bsObj = BeautifulSoup(driver.page_source,'html.parser')


page_option = bsObj.find('select',id="AspNetPager1_input").findAll('option')
page_length = int(page_option[len(page_option)-1].get_text())    #获得所有页数

columns = bsObj.findAll(style="padding-top: 1px;")
#columns_text = get_plain_text(columns)
columns_text = scrap.get_plain_text(columns)
columns_text.insert(0,'排名')


group_option = bsObj.find('div',{"class":"fl"}).find('dd').findAll('a')
group_name = []   #采集所有group的名字
for i in group_option:
    group_name.append(i.get_text().split()[0])
group_name.remove(group_name[-1])  #删除期权，比赛未做要求

date_list = []
date_list = dt.get_date_list('2016-04-01','2016-9-30')  #获得所有日期

def main():
    #user_information = scrap.select_data(user_information,driver)  #收集第一页信息

    #logging.debug('Now group is:%s', group_name[scrap.get_group_now(group_name,driver) - 1])
    '''
    for i in range(page_length-1):   #收集剩余页信息测试
        page = scrap.next_page(page,driver)
        user_information = scrap.select_data(user_information,driver)
    '''

    '''
    for i in range(len(group_name) - 1):
        scrap.next_group(group_name,driver) #收集剩余组信息测试
        user_information = scrap.select_data(user_information,driver)
    '''
    #scrap.go_to_day('2016-08-17',driver)
    #scrap.go_to_day('2016-07-15',driver)
    '''
    for date in date_list[0:5]:
        scrap.go_to_day(date,driver)
        user_information = scrap.select_data(user_information,driver)

    df = pd.DataFrame(user_information,columns = columns_text) #使用pandas储存数据
    df.to_csv('test.csv',index=False)
    '''
    #采集有重大bug!
    '''
    我们的采集顺序：每页->每组->每日
    '''
    for date in date_list:
        scrap.go_to_day(date,driver)   #到达指定的date
        #user_information = scrap.select_data(user_information,driver) #收集第一组信息
        for group_i in range(len(group_name)):
            user_information = []  #每采集某一组时，重新开始建立pandas文件

            #因为page在不同组或者不同日下会有变化，每次获取某日某组所有日之前需要获取最新的页数
            page_option = bsObj.find('select',id="AspNetPager1_input").findAll('option')
            page_length = int(page_option[len(page_option)-1].get_text())    #获得所有页数

            page = 1   #每采集某一组时，重新开始记页
            #user_information = scrap.select_data(user_information,driver) #爬第一页的数据
            for page_j in range(page_length):  #爬剩余页数据
                user_information = scrap.select_data(user_information,driver)
                try:
                    page = scrap.next_page(page,driver)
                except Exception as e:
                    print("No page left.")
            df = pd.DataFrame(user_information,columns = columns_text) #使用pandas储存数据
            df.to_csv(group_name[group_i]+'-'+date+'.csv',index=False) #每采集完一日的一组后，存储一次
            try:
                scrap.next_group(group_name,driver)
            except Exception as e:
                print("Last group")



if __name__ == "__main__":
    main()

logging.debug('End of program')
