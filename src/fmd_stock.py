from fmd import FmdApi
import pandas as pd

fa = FmdApi()
etf = fa.etf.get('0056')
dividend = etf.get_dividend(start_year=2016, end_year=2024)

df = pd.DataFrame(dividend)
df.to_csv('0056_dividend.csv', index=False)


'''
# example: tsmc 2330

from fmd import FmdApi
import pandas as pd

fa = FmdApi()
stock = fa.stock.get('2330')
dividend = stock.get_dividend()

df = pd.DataFrame(dividend)
df.to_csv('2330_stock_dividend.csv', index=False)

'''