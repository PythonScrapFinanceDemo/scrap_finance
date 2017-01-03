from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import logging
import pandas as pd
import numpy as np


#清洗掉数据中的垃圾，该函数只针对columns_text，看起来是个失败
def get_plain_text(ResultSet):
    text = []
    for i in ResultSet:
        text.append(i.get_text().split()[0])    #因为split()返回的是字符串列表，所以要加[0]
    return text

#读取数据，提取并清洗数据，最后装入user_information中
def select_data(user_information,driver):
    bsObj = BeautifulSoup(driver.page_source,'html.parser')
    user_information_obj = bsObj.findAll('tr',style="background: #fff;")
    for i,user_i in enumerate(user_information_obj):
        temp = []
        for td_i in user_i.findAll("td"):
            temp_data = td_i.get_text().split()
            if not temp_data:     #无数据
                temp.append("")
            else:
                temp.append(temp_data[0])
        user_information.append(temp)
    return user_information


def get_page_now(driver):  #获取当前所在页数，并返回
    bsObj = BeautifulSoup(driver.page_source,'html.parser')
    #page_now = int(bsObj.find('select',id="AspNetPager1_input").find('option',selected="true").get_text())
    try:
        page_now = int(bsObj.find('select',id="AspNetPager1_input").find('option',selected="true").get_text())
    except Exception as e:
        print("Can't get page_now!")
    else:
        return page_now

def get_group_now(group_name,driver):  #获取当前所在group的id，并返回
    bsObj = BeautifulSoup(driver.page_source,'html.parser')
    try:
        group_now = group_name.index(bsObj.find('div',{"class":"fl"}).find('dd').find('a',{"class":"select"}).get_text().split()[0]) + 1
        #index()方法返回一个item在list中的位置，此处加1,是为了与dom中id从1开始相匹配，dom中链接的id为lbAccountType+i
    except Exception as e:
        print("We can't get the group_now!")
    else:
        return group_now

def get_next_page_button(driver):  #找到下一页的按钮并返回按钮
    page_now = get_page_now(driver)
    page_next = str(page_now + 1)
    try:
        if page_now%10 != 0:
            #next_page_button = driver.find_element_by_xpath("//a[@title='转到第'+page_next+'页']")
            next_page_button = driver.find_element_by_link_text('['+page_next+']')
        else:
            next_page_button = driver.find_elements_by_link_text('...')[-1]
        #next_page_button = driver.find_element_by_link_text('&gt;')
    except Exception as e:
        print("We can't get the next page button!")
        raise e
    else:
        return next_page_button

def get_next_group_button(group_name,driver):
    group_now = get_group_now(group_name,driver)
    # attention!这里的get_group_now返回的是下标加1的位置！即下标从1开始计数！
    group_next = group_now + 1
    try:
        assert(group_next<=len(group_name))
        next_group_button = driver.find_element_by_id("lbAccountType"+str(group_next))
    except Exception as e:
        print("We can't get the next group button!")
    else:
        return next_group_button

def next_page(page,driver):    #翻页，并返回当前所在页数
    next_page_button = get_next_page_button(driver)
    try:
        next_page_button.click()   #模拟点击
    except Exception as e:
        print("blank page_button or other wrong!")
        raise e

    page_now = get_page_now(driver)

    logging.debug('Now page is:%s', page_now)
    page = page + 1
    logging.debug('The page we record is:%s', page)
    assert(page==page_now)
    return page

def next_group(group_name,driver):    #切换到下一个组
    next_group_button = get_next_group_button(group_name,driver)
    try:
        next_group_button.click()
    except Exception as e:
        print("can't click the next group button! or other wrong!")
        raise e
    logging.debug('Now group is:%s', group_name[get_group_now(group_name,driver) - 1])
    #为什么要减一呢？因为get_group_now函数返回的是下标加一

def go_to_day(day,driver):    #切换到指定某一天
    search_button = driver.find_element_by_id("ibSearch")
    day_input_text = driver.find_element_by_id("txtTradeDate")
    day_input_text.clear()     #清空字符
    day_input_text.send_keys(day)  #填充字符
    try:
        #assert()
        search_button.click()  #点击搜索按钮
        day_input_text = driver.find_element_by_id("txtTradeDate")
        logging.debug('Now day is:%s', day_input_text.get_property("value"))
    except Exception as e:
        print("We can't go to the day! Or other wrong!")
        raise e
