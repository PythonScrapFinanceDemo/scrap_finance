from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://spds.qhrb.com.cn/SP10/SPOverSee1.aspx")
#html = urlopen("data.html")
bsObj = BeautifulSoup(html.read(),'lxml')

def get_plain_text(ResultSet):
    text = []
    for i in ResultSet:
        text.append(i.get_text())
    return text

columns = bsObj.findAll(style="padding-top: 1px;")
columns_text = get_plain_text(columns)

'''
users = bsObj.findAll(style='color:#0000FF;')
users_texts = get_plain_text(users)
'''

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

for user_i in user_information_obj:
    #user_length.append(user_i.)
