from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import logging
import pandas as pd

import package_scrap.scrap as scrap
import package_scrap.date as dt

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')

url = "http://spds.qhrb.com.cn/SP10/SPOverSee1.aspx"

#driver = webdriver.Chrome("/usr/local/chromedriver-Linux64")
driver = webdriver.PhantomJS()
driver.get(url)

bsObj = BeautifulSoup(driver.page_source,'html.parser')

group_option = bsObj.find('div',{"class":"fl"}).find('dd').findAll('a')
group_name = []   #采集所有group的名字
for i in group_option:
    group_name.append(i.get_text().split()[0])
group_name.remove(group_name[-1])  #删除期权，比赛未做要求

date_list = []
date_list = dt.get_date_list('2016-04-01','2016-09-30')  #获得所有日期

def main():
    '''
    我们的采集顺序：每页->每组->每日
    '''
    for date in date_list:
        scrap.go_to_day(date,driver)   #到达指定的date
        scrap.click_first_page(driver) #点击一下首页或者do nothing

        for group_i in range(len(group_name)):
            if scrap.click_first_page(driver): #点击一下首页或者do nothing
                user_information = []  #每采集某一组时，重新开始建立pandas文件

                #因为page在不同组或者不同日下会有变化，每次获取某日某组所有日之前需要获取最新的页数
                bsObj = BeautifulSoup(driver.page_source,'html.parser')
                page_option = bsObj.find('select',id="AspNetPager1_input").findAll('option')
                page_length = int(page_option[len(page_option)-1].get_text())    #获得所有页数

                page = 1   #每采集某一组时，重新开始记页
                for page_j in range(page_length - 1):  #爬剩余页数据
                    user_information = scrap.select_data(user_information,driver)
                    page = scrap.next_page(page,driver)
                user_information = scrap.select_data(user_information,driver) #收集最后一页后，不再翻页

                columns = bsObj.findAll(style="padding-top: 1px;")
                columns_text = scrap.get_plain_text(columns)
                columns_text.insert(0,'排名')

                df = pd.DataFrame(user_information,columns = columns_text) #使用pandas储存数据
                df.to_csv(group_name[group_i]+'-'+date+'.csv',index=False) #每采集完一日的一组后，存储一次

            if group_i < len(group_name) - 1:  #到最后一组时不再进入下一组
                scrap.next_group(group_name,driver)
            else:
                pass



if __name__ == "__main__":
    main()

logging.debug('End of program')
