import pandas as pd
from pandas import Series,DataFrame
import csv
import os


def get_date(filename):
    date = filename.split('-')
    return date[1]+'-'+date[2]+'-'+date[3]

def all_to_one(nameList):
    '''
    所有csv文件合并到一个csv文件里，命名为`total_temp.csv`，以便后续处理。
    '''
    for df_i in range(len(nameList)):
        df_name = nameList[df_i]+'.csv'
        temp_df = pd.read_csv(df_name, low_memory=False)
        if df_i == 0:
            total_df = temp_df
        else:
            total_df = total_df.append(temp_df,ignore_index=True)
    total_df.to_csv('total_temp.csv')
    return total_df

def deal_csv(folderName,label=0):
    '''
    处理抓取的数据,将一组的所有交易日数据合并到一个csv文件里，用组别命名
    '''
    filetowrite=open(folderName+'.csv','a')
    writer=csv.writer(filetowrite)

    files = []  #存储所有的csv文件名
    for (dirpath, dirnames, filenames) in os.walk(folderName):
        files.extend(filenames)
        break

    for file_i in range(len(files)):
        filename = files[file_i]
        temp_df = pd.read_csv(os.path.join(folderName,filename))
        temp_df['时间'] = Series(get_date(filename),index=temp_df.index)
        temp_df['排行榜'] = Series(folderName,index=temp_df.index)
        if '组别' not in temp_df.columns:
            temp_df['组别'] = Series('-',index=temp_df.index)
        if label == 1:
            temp_df['净利润得分'] = Series('-',index=temp_df.index)
            temp_df['回撤率得分'] = Series('-',index=temp_df.index)
            temp_df['净值得分'] = Series('-',index=temp_df.index)
            temp_df['综合得分'] = Series('-',index=temp_df.index)
        temp_df['客户代码'] = Series('-',index=temp_df.index) #先设置为‘-’，以后再判断
        cols = temp_df.columns.tolist()
        cols.sort()
        temp_df = temp_df[cols]
        temp_df.to_csv('temp_df.csv')
        filetoread=open('temp_df.csv','r')
        reader=csv.reader(filetoread)
        if file_i != 0:
            for i,line in enumerate(reader):
                if i != 0:
                    writer.writerow(line)
        else:
            for line in reader:
                writer.writerow(line)
        print(file_i)
    filetowrite.close()

def chenge_columns_order(columns_list):
    '''
    更改混乱的columns的顺序，将columns的顺序定义为传入的`columns_list`的顺序。生成一个新的csv文件`total_temp_nc.csv`
    '''
    temp_df = pd.read_csv('total_temp.csv', low_memory=False)
    temp_df = temp_df[columns_list]
    temp_df.to_csv('total_temp_nc.csv')

def sort_df():
    '''
    按照客户昵称和排名的顺序进行排序，得到新的csv文件`total_temp_new.csv`。
    '''
    temp_df = pd.read_csv('total_temp_nc.csv', low_memory=False)
    temp_df = temp_df.sort_values(['客户昵称','排名'], ascending=[True,True])
    temp_df.to_csv('total_temp_new.csv')


def make_unique(original_list):
    unique_list = []
    [unique_list.append(obj) for obj in original_list if obj not in unique_list]
    return unique_list

def get_id():
    '''
    根据用户昵称为用户添加ID。得到新的文件`total_temp_new_id.csv`。 
    '''
    temp_df = pd.read_csv('total_temp_new.csv', low_memory=False)
    names = make_unique(temp_df['客户昵称'].tolist())
    temp_df['ID'] = Series('-',index=temp_df.index)
    order = 0
    for i in range(len(names)):
        print(i)
        nums  = len(temp_df[temp_df['客户昵称']==names[i]])
        temp_df['ID'].loc[order:order+nums] = i
        order = order + nums
    temp_df.to_csv('total_temp_new_id.csv')

if __name__ == '__main__':
    deal_csv('JiJinZu')
    deal_csv('ChengXuHuaZu')
    deal_csv('QingLiangZu')
    deal_csv('ZhongLiangZu')
    deal_csv('GuiJinShu',1)
    deal_csv('NongChanPin',1)
    deal_csv('NengYuanHuaGong',1)
    deal_csv('YouSeJinShu',1)
    deal_csv('JinRongQiHou',1)
    deal_csv('JingLiRun',1)
    all_to_one(['JiJinZu','ChengXuHuaZu','QingLiangZu','ZhongLiangZu','GuiJinShu','NongChanPin','NengYuanHuaGong','YouSeJinShu','JinRongQiHou','JingLiRun'])

    columns_list = ['客户昵称','组别','排行榜','时间','排名','当日权益','风险度(%)','净利润','净利润得分','回撤率(%)','回撤率得分','日净值','累计净值',
                    '净值得分','综合得分','参考收益率(%)','指定交易商','操作指导','账户评估']

    chenge_columns_order(columns_list)

    sort_df()
    get_id()
