# 爬虫文档
该程序主要使用了BeautifulSoup,selenium,pandas,datetime,calendar这几个python库。  
我们将所需要调用的方法都放在一个叫做package_scrap的包里，以便于主函数分离。  
selenium主要负责模拟点击操作，使用PhantomJS这个不带图形界面的浏览器，可以减轻计算资源压力。  
BeautifulSoup是一个著名的爬虫库，简单易学。  
我们使用logging库以便于观察程序运行状况，如果出现错误可以发现错误所在。  
datetime和calendar是用来对付日期和时间的。  

下面我们来分析一下主要的程序部分
先看主函数main.py：  
```
url = "http://spds.qhrb.com.cn/SP10/SPOverSee1.aspx"
driver = webdriver.PhantomJS()
```
上述代码用selenum获取driver，以便后续的模拟操作。  
```
bsObj = BeautifulSoup(driver.page_source,'html.parser')
group_option = bsObj.find('div',{"class":"fl"}).find('dd').findAll('a')
group_name = []   #采集所有group的名字
for i in group_option:
    group_name.append(i.get_text().split()[0])
group_name.remove(group_name[-1])  #删除期权，比赛未做要求
```
这一段就是获取比赛要求的十个参赛组的名称。  

```
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

```
1. 主函数部分：  
 我们传入一个date_list,这个date_list是一个列表文件，里面存储了从4月1号到9月30号的所有交易日日期，剔除了周末和法定假期等非交易日。  
我们的抓取顺序是最外面的循环每次是日期的循环，第二层循环是10个参赛组的循环，第三层循环是每日每组时页数的循环。  
 - 日期的循环：  
 每次完成一日的抓取后，`go_to_day`方法模拟日期填表下一个交易日，然后点击提交按钮，因为进入下一页后对应的页数往往不是第一页，所以我们使用`click_first_page`方法模拟点击翻页到第一页。  
参赛组的循环：我们存储未经处理的原始数据时将每一日每一组的数据放到一个csv文件里（最后我们再将其合并成一个整体的csv文件），并按照组别+日期的方式规范命名，以便后续处理。
 每次模拟点击进入一组参赛组后，先获取该日该组的页数，然后进入页数的循环。
 页数的循环会返回一个list形式存储的数据`user_information`，然后我们获得该组对应的每列名称，存到`columns_text`中，将其作为即将存储的DataFrame的`columns`，将`user_information`导入DataFrame.最后我们将这个DataFrame转换为csv形式，存到本地。  
 - 页数的循环：  
 我们使用了一个`select_data`方法来获取当前页下所有的数据，并以list的形式返回。

2. `scrap.py`部分：  
```
def select_data(user_information,driver):
    bsObj = BeautifulSoup(driver.page_source,'html.parser')
    try:
        user_information_obj = bsObj.findAll('tr',style="background: #fff;")
    except Exception as e:
        print("No datas")
    else:
        for i,user_i in enumerate(user_information_obj):
            temp = []
            for td_i in user_i.findAll("td"):
                temp_data = td_i.get_text().split()
                if not temp_data:     #无数据
                    temp.append("-")
                else:
                    temp.append(temp_data[0])
            user_information.append(temp)
        return user_information
```
`scrap.py`存储了我们在主函数里调用的所有和模拟点击，抓取信息有关的函数。
我们分析其中主要的几个起到关键作用的函数：  

`select_data(user_information,driver)`：  
该函数用来抓取当前`driver`对应的页面的数据。`user_information`是一个list，用于存储抓取的信息。  
先使用bs库的BeautifulSoup方法获取当前页面的html代码，然后开始存储：  
经观察网站的html代码，所有的数据都在一个table里，而我们要抓取的信息，每一行是在一个`tr`标签里，它们的共同点是`style="background: #fff;`,可以用来区分与其他非数据`tr`标签。  
我们获取所有的`tr`标签：`user_information_obj = bsObj.findAll('tr',style="background: #fff;")`。  
当没有异常抛出时，进入`else`作用域：  
循环操作这个`user_information_obj`：新建一个临时的空list:`temp`，每一行对应的数据，都分别存储在这一行对应的`tr`标签的`td`子标签中，我们就再对每一个`td`子标签进行循环操作，提取其中对应的字符串信息：`temp_data = td_i.get_text().split()`,然后把他们都添加到`temp`中，最后再将这个临时list添加到`user_information`中，在下一次对`tr`的循环置空`temp`。  
完成两层循环后，返回`user_information`。  

`get_page_now(driver)`方法用于获取当前页对应的页码，该方法主要是方便其他方法调用。  
```
def get_page_now(driver):  #获取当前所在页数，并返回
    bsObj = BeautifulSoup(driver.page_source,'html.parser')
    try:
        page_now = int(bsObj.find('select',id="AspNetPager1_input").find('option',selected="true").get_text())
    except Exception as e:
        print("Can't get page_now!")
    else:
        return page_now
```
观察网页的html代码，页码可以在`select`块中观察到，`select`对应的`id`为`AspNetPager1_input`。`select`块中有`option`标签，当`option`的`selected="true"`时，其对应的字符串就是当前页码。  

`get_group_now(group_name,driver):`方法用于获取当前组对应的ID，原理与`get_page_now`类似。不再赘述。  

`get_next_page_button(driver)`方法用于找到下一页的链接，并模拟点击，进入下一页，以便继续抓取数据。  
```
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
        print("We at page: "+str(page_now))
        print("We can't get the next page button!")
        raise e
    else:
        return next_page_button
```
先用get_page_now获取当前页数，加1就是下一页，之后分析HTML代码，获得下一页链接，返回driver对应的element.  

`get_next_group_button(group_name,driver)`获得下一组的链接并模拟点击，原理类似，不再赘述。  

`next_page(page,driver)`方法通过`get_next_page_button(`返回的元素，模拟点击翻页操作的行为。进行翻页。  

`next_group(group_name,driver)`方法通过`get_next_group_button`返回的元素，模拟点击下一参赛组的行为。进入下一参赛组。  

`click_first_page(driver)`因为在每次翻页或切换组时有可能第一次看到的页码不是第一页，所以模拟点击第一页的链接。  

`go_to_day(day,driver)`该方法指定切换到传入的参数day对应的日期，模拟填表，然后发送请求。是日期切换到指定日期。  

3. `date.py` 部分  
该部分主要使用`datetime`和`calendar`两个类库，来获取所有从4.1到9.30之间的所有交易日列表。  
`get_date_list(begin_date,end_date)`方法接收起止日期的字符串，剔除掉所有法定节假日。返回交易日列表。  

`tick_weekend(date_list)`方法用于辅助`get_date_list`剔除掉所有的周末。  

4. `deal_csv.py` 部分  
`deal_csv(folderName,label=0)`方法用于处理抓取的数据，使用os模块获取所有已爬取的csv文件，一次运行针对一个特定组别，因为前四个参赛组和后六个参赛组columns信息数不同，所以通过传入的label来判断是否添加column，以便于后续的合并，该方法最后将一组的所有交易日数据合并到一个csv文件里，用组别命名。  

`all_to_one(nameList)`方法将`deal_csv(folderName,label=0)`生成的所有csv文件合并到一个csv文件里，命名为`total_temp.csv`，以便后续处理。期间按照客户昵称和排名的顺序进行排序，并根据用户昵称为用户添加ID，得到新的文件`total_data.csv`。  
