import pandas as pd
from pandas import Series,DataFrame
import csv
import os


def get_date(filename):
    date = filename.split('-')
    return date[1]+'-'+date[2]+'-'+date[3]

def all_to_one(nameList,columns_list):
    for df_i in range(len(nameList)):
        df_name = nameList[df_i]+'.csv'
        temp_df = pd.read_csv(df_name, low_memory=False)
        if df_i == 0:
            total_df = temp_df
        else:
            total_df = total_df.append(temp_df,ignore_index=True)
    temp_df = total_df
    temp_df = temp_df[columns_list]
    temp_df = temp_df.sort_values(['客户昵称','排名'], ascending=[True,True])
    names = make_unique(temp_df['客户昵称'].tolist())
    temp_df['ID'] = Series('-',index=temp_df.index)
    order = 0
    for i in range(len(names) - 1):
        print(i)
        nums  = len(temp_df[temp_df['客户昵称']==names[i]])
        temp_df['ID'].loc[order:order+nums] = i
        order = order + nums
    temp_df.to_csv('total_data.csv')
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


if __name__ == '__main__':
    deal_csv('基金组')
    deal_csv('程序化组')
    deal_csv('轻量组')
    deal_csv('重量组')
    deal_csv('贵金属',1)
    deal_csv('农产品',1)
    deal_csv('能源化工',1)
    deal_csv('有色金属',1)
    deal_csv('金融期货',1)
    deal_csv('净利润',1)

    columns_list = ['客户昵称','组别','排行榜','时间','排名','当日权益','风险度(%)','净利润','净利润得分','回撤率(%)','回撤率得分','日净值','累计净值',
                    '净值得分','综合得分','参考收益率(%)','指定交易商','操作指导','账户评估']
    all_to_one(['基金组','程序化组','轻量组','重量组','贵金属','农产品','能源化工','有色金属','金融期货','净利润'],columns_list)
