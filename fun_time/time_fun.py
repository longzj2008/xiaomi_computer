import datetime
import os
import pandas as pd

def time_now():
    #返回当前时间
    now = datetime.datetime.now()
    return(now)

def fun_now_after(period_str):
    now=time_now()
    now_after=now-datetime.timedelta(days=eval(period_str))
    return (now_after)

def makedir(path):
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)

#使用时需要更改保存的文件类型和名称
def save(df_data,path):
        now=time_now()
        file_name=now.strftime('%Y-%m-%d %H_%M_%S')+'.xlsx'
        makedir(save_folder_path)       #检查结果存放路径是否存在！
        file_path=os.path.join(save_folder_path,file_name)
        df_data.to_excel(file_path)
        # df1.to_csv(file_path,header=None,index=None,sep=' ',mode='a')

def url_date_list(date_till,num):
    date_t=datetime.datetime.strptime(date_till,'%Y%m%d')
    ls_date = []
    for i in range(eval(num)):
        date_temp = date_t - datetime.timedelta(days=i)
        date = date_temp.strftime('%Y%m%d')
        url_date=r'/diary/'+date
        ls_date.append(url_date)
    return (ls_date)

if __name__ =='__main__':
    # path = r'v:\Test_rig_public_information'
    # url_date_list()
    # rr='dfad'
    # date='/diary/20180623/p.2'
    # path = 'ds_data/' + date.replace('/', '').replace('.', '')[5:] + '.csv'
    # print(path)
    # # with open(path,'w') as f:
    # #     f.write(rr)
    date='20180630'
    num='2'

    ls=url_date_list(date,num)
    print(ls)