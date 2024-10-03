import twstock
import pandas as pd

# plot
import matplotlib
import mplfinance as mpf

# os
from pathlib import Path

Path("./data/").mkdir(parents=True, exist_ok=True)


def fetch_raw(target_stock, year, month):
    stock = twstock.Stock(target_stock)
    target_price = stock.fetch_from(year, month)

    df = pd.DataFrame(columns = name_attribute, data = target_price)

    filename = f'./data/{target_stock}.csv'
    df.to_csv(filename)
    
def plot(target_stock):
    df = pd.read_csv(f'./data/{target_stock}.csv', parse_dates=True, index_col=1) #讀取目標股票csv檔的位置

    df.rename(columns={'Turnover':'Volume'}, inplace = True) 
    #這裡針對資料表做一下修正，因為交易量(Turnover)在mplfinance中須被改為Volume才能被認出來

    mc = mpf.make_marketcolors(up='r',down='g',inherit=True)
    s  = mpf.make_mpf_style(base_mpf_style='yahoo',marketcolors=mc)
    #針對線圖的外觀微調，將上漲設定為紅色，下跌設定為綠色，符合台股表示習慣
    #接著把自訂的marketcolors放到自訂的style中，而這個改動是基於預設的yahoo外觀

    kwargs = dict(type='candle', mav=(5,20,60), volume=True, figratio=(10,8), figscale=0.75, title=target_stock, style=s) 
    #設定可變參數kwargs，並在變數中填上繪圖時會用到的設定值

    mpf.plot(df, **kwargs)
    #選擇df資料表為資料來源，帶入kwargs參數，畫出目標股票的走勢圖

# stock form define
## [日期 總成交股數 總成交金額(Volume) 開 高 低 收 漲跌幅 成交量]
name_attribute = ['Date', 'Capacity', 'Turnover', 'Open', 'High', 'Low', 'Close', 'Change', 'Transcation']
# name_attribute = ['Date', '總成交股數', '總成交金額', '開', '高', '低', '收', '漲跌幅', '成交量']

# time period (the raw from date stamp to now)
year = 2010
month = 1

if __name__ == '__main__':
    
    # stock
    target_stock = '3034'
    
    fetch_raw(target_stock, year, month)
    # plot(target_stock)

    print()