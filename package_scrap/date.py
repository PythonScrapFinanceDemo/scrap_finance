import datetime
import calendar

def get_date_list(begin_date,end_date):
    '''
    输入日期格式为列表'year-month-day'
    该方法仅适用于该爬虫，如果改变日期会出现重大bug
    起始日期必须是月首日或月末日
    说实话这个方法写的非常之烂，原因是我很懒，以后闲的蛋疼的话我再修改
    '''
    begin_date = begin_date.split('-')
    end_date = end_date.split('-')
    date_list = []
    begin_year = begin_date[0]
    begin_month = begin_date[1]
    begin_day = begin_date[2]
    end_year = end_date[0]
    end_month = end_date[1]
    end_day = end_date[2]
    exclude_date = ['2016-04-02','2016-04-03','2016-04-04','2016-04-30','2016-05-01','2016-05-02','2016-06-09','2016-06-10','2016-06-11','2016-06-12','2016-09-15','2016-09-16','2016-09-17','2016-09-18']
    if int(begin_year) == int(end_year):
        total_month = int(end_month) - int(begin_month) + 1
        for month_id in range(total_month):
            month_end_day = calendar.monthrange(int(begin_year),month_id+int(begin_month))[1]
            #获得该月份实际天数
            for day_id in range(1,month_end_day+1):
                month_temp = str(month_id+int(begin_month))
                if len(month_temp) == 1: #必须写成0x的形式
                    month_temp = '0'+month_temp
                day_temp = str(day_id)
                if len(day_temp) == 1:
                    day_temp = '0'+day_temp
                date_temp = begin_year+'-'+month_temp+'-'+day_temp
                #这个网站自动适配日期做的还可以，2016-7-1这样的也是符合要求的
                #此话作废，我真高估了前端的智商，这个网站就是个垃圾！
                if date_temp not in exclude_date:
                    date_list.append(date_temp)
                #date_list.append(date_temp)
    else:
        print("I have to do some change in my function!")
        print("按理说根据需求不会出现这种情况，如果出现，程序的健壮性需要改善。")

    date_list = tick_weekend(date_list)
    return date_list

def tick_weekend(date_list):
    date_without_weekend = []
    for date in date_list:
        date_temp = date.split("-")
        weekday = calendar.weekday(int(date_temp[0]),int(date_temp[1]),int(date_temp[2]))
        if weekday != 0 and weekday != 6:
            date_without_weekend.append(date)
    return date_without_weekend


if __name__ == "__main__":
    #仅供测试
    begin_date = input("begin_date:  ")
    end_date = input("end_date:   ")
    date_list = get_date_list(begin_date,end_date)
    print(date_list)
