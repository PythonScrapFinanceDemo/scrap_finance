import pandas as pd
from pandas import Series,DataFrame
import numpy as np
import csv
import sys,os


def get_date(filename):
    date = filename.split('-')
    return date[1]+'-'+date[2]+'-'+date[3]

def rebuild_csv(folderName):  #适用于程序化组以及和其类似的组
    files = []  #存储所有的csv文件名
    for (dirpath, dirnames, filenames) in os.walk(folderName):
        files.extend(filenames)
        break

    for file_i in range(len(files)):
        filename = files[file_i]
        if file_i == 0:
            temp_df = pd.read_csv(os.path.join(folderName,filename))
            temp_df['时间'] = Series(get_date(filename),index=temp_df.index)
            temp_df['排行榜'] = Series(folderName,index=temp_df.index)
            if '组别' not in temp_df.columns:
                temp_df['组别'] = Series('-',index=temp_df.index)
            df = temp_df
        else:
            temp_df = pd.read_csv(os.path.join(folderName,filename))
            temp_df['时间'] = Series(get_date(filename),index=temp_df.index)
            temp_df['排行榜'] = Series(folderName,index=temp_df.index)
            if '组别' not in temp_df.columns:
                temp_df['组别'] = Series('-',index=temp_df.index)
            df = df.append(temp_df,ignore_index=True)
    df.to_csv(folderName+'.csv',index=False)

'''
temp codes:

temp.sort('排名', ascending=False)
'''


if __name__ == '__main__':
    #rebuild_csv('轻量级组')
    rebuild_csv(input("输入文件夹名：  "))
