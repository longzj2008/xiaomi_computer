import random
import time
import pandas as pd
from bs4 import BeautifulSoup
from fun_get_id import main_get_id
from fun_get_sp_xc import main_get_sp_xc,main_get_xc_table


def fun_download_driver_url(driver,url):
    driver.get(url)
    t=random.randint(20,30) # 设置随机延时，防止被封号
    time.sleep(t/10)
    html = driver.page_source.encode('utf-8')
    html_soup = BeautifulSoup(html, 'lxml')
    return (html_soup)

def function_Event_log_record(error_flag,content):
    if error_flag == 1:
        with open('data\ErrorLog.txt', 'a') as f:
            f.write(content)

def download_sp41_xc_table_base_id(id,driver,path_save_prefix,date_path):
    print(id)
    url_main = 'https://www.dszuqiu.com'
    ##############################################
    #从现场页面中药提取两个数据
    url_id = url_main + r'/race_xc/' + str(id)
    print(url_id)
    html_soup = fun_download_driver_url(driver, url_id)
    ############################################################################################################
    # 提取ID现场 中的 图文信息及半场，全场数据信息
    ############################################################################################################
    sr_xc_id, error = main_get_sp_xc.fun_main_get_data_xc(html_soup)
    function_Event_log_record(error,url_id)
    #df_xc_all = df_xc_all.append(sr_xc_id, ignore_index=True)  # df append()之后，必需重新赋值给df，不然df还使用原来的
    ############################################################################################################
    # 下载ID现场 中的 表格信息
    ############################################################################################################
    try:
        df_xc_table = main_get_xc_table.fun_main_adjust_gongfang_table(html_soup)
    except:
        df_xc_table = pd.DataFrame()
    path = path_save_prefix + 'ds_data_xc_table//' + date_path + '_' + str(id) + '.csv'
    df_xc_table.to_csv(path, encoding='utf-8')
    ############################################################################################################
    # 下载 4和1 数据
    ############################################################################################################
    url_id = url_main + r'/race_sp/' + str(id)
    print(url_id)
    html_soup = fun_download_driver_url(driver, url_id)
    try:
        df_sp41 = main_get_sp_xc.fun_main_get_data_sp(html_soup)
    except:
        df_sp41 = pd.DataFrame()
    path = path_save_prefix + 'ds_data_sp41//' + date_path + '_' + str(id) + '.csv'
    df_sp41.to_csv(path)
    return (sr_xc_id)
    pass

if __name__=='__main__':
    pass