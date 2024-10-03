from urllib.parse import urlencode, urljoin
# from datetime import datetime
import datetime
from pandas.core.frame import DataFrame
import requests
import pandas as pd




def get_etf_dividend_history(
        symbol: str = "", 
        # start_date: str = '20050101', 
        start_date: str = (datetime.datetime.now()+datetime.timedelta(days=-30)).strftime('%Y%m%d'), 
        end_date: str = datetime.datetime.now().strftime('%Y%m%d'),
    ) -> dict:

    base_url = 'https://www.twse.com.tw/rwd/zh/ETF/etfDiv'
    params = {
        'stkNo': symbol,
        'startDate': start_date,
        'endDate': end_date,
        'response': 'json',
    }
    query_string = f'?{urlencode(params)}'
    res = requests.get(urljoin(base_url, query_string))

    if res.status_code == 200:
        return res.json()
    else:
        raise Exception(f'Get data fail. {res.text}')


def map_fields_and_values(source: dict) -> DataFrame:
    fields = source.get('fields')
    data = source.get('data')
    output = {}
    for idx, row in enumerate(data):
        output.setdefault(
            idx,
            {
                k: v
                for k, v in zip(fields, row)
            }
        )
    df = pd.DataFrame(output).T
    return df


def handle_date(v: str) -> datetime:
    return datetime.datetime.strptime(
        f'{int(v[0:3])+1911}-{v[4:6]}-{v[7:9]}', 
        '%Y-%m-%d',
    )


def create_customize_dividend_table(df: DataFrame) -> DataFrame:
    required_fields = [
        '證券代號',
        '證券簡稱',
        '除息交易日',
        '收益分配發放日',
        '收益分配金額 (每1受益權益單位)',
    ]
    dividend_df = df[required_fields].copy()

    dividend_df['除息交易日'] = dividend_df['除息交易日'].apply(handle_date)
    dividend_df['收益分配發放日'] = dividend_df['收益分配發放日'].apply(handle_date)

    fields_chi_to_en = {
        '證券代號': 'symbol',
        '證券簡稱': 'short_name',
        '除息交易日': 'ex_dividend_date',
        '收益分配基準日': 'dividend_based_date',
        '收益分配發放日': 'dividend_receive_date',
        '收益分配金額 (每1受益權益單位)': 'dividend_amount',
        '收益分配標準 (102年度起啟用)': 'dividend_detail',
        '公告年度': 'year'
    }
    dividend_df.rename(columns=fields_chi_to_en, inplace=True)
    return dividend_df


data = get_etf_dividend_history()
df = map_fields_and_values(data)
dividend_df = create_customize_dividend_table(df)
dividend_df.to_csv('etf_dividend.csv', index=False)

print()