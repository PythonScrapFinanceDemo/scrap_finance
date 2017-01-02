from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import logging
import pandas as pd
import numpy as np


def get_plain_text(ResultSet):
    text = []
    for i in ResultSet:
        text.append(i.get_text().split()[0])    #因为split()返回的是字符串列表，所以要加[0]
    return text

def select_data(user_information,driver):   #提取并清洗数据
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


def get_page_now(driver):  #获取当前页数
    bsObj = BeautifulSoup(driver.page_source,'html.parser')
    #page_now = int(bsObj.find('select',id="AspNetPager1_input").find('option',selected="true").get_text())
    try:
        page_now = int(bsObj.find('select',id="AspNetPager1_input").find('option',selected="true").get_text())
    except Exception as e:
        print("Can't get page_now!")
    else:
        return page_now


def get_next_page_button(driver):  #返回按钮
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


def next_page(page,driver):
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
