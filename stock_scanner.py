from stockstats import StockDataFrame
from nsepy import get_history
from utils import get_datestr_to_date
import pandas as pd
import io
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--start_date', action="store", help="Start Data", type=str)
parser.add_argument('--end_date', action="store", help="end_data", type=str)
parser.add_argument('--ema_day', action="store", help="EMA days", type=int)
parser.add_argument('--last_days_count', action="store", help="Latest days to consider", type=int)

NIFTY_50_URL = 'https://www.nseindia.com/content/indices/ind_nifty50list.csv'
NIFTY_NEXT_50_URL = 'https://www.nseindia.com/content/indices/ind_niftynext50list.csv'


class StockScanner(object):
    """
    """
    def __init__(self, **kwargs):
        """
        """
        self.start_date = kwargs.get('start_date')
        self.end_date = kwargs.get('end_date')
        self.stocks_info_list = []

    def _get_history(self, symbol):
        """
        :return:
        """
        return get_history(symbol=symbol, start=get_datestr_to_date(self.start_date),
                           end=get_datestr_to_date(self.end_date))

    def _get_stock_symbols(self):
        """For Now Get Nifty 50 and Nifty Next 50 Stocks for Scanning
        :return:
        """
        # TODO: Web Scrap Nse Web Site to get Nifty 50 and Nifty next 50 Stocks Symbol
        s = requests.get(NIFTY_50_URL).content
        nifty_df = pd.read_csv(io.StringIO(s.decode('utf-8')))
        s = requests.get(NIFTY_NEXT_50_URL).content
        nifty_next_df = pd.read_csv(io.StringIO(s.decode('utf-8')))
        df = nifty_df.append(nifty_next_df)
        return df.Symbol

    def scan_stocks(self):
        """
        Perform Scanning of Stocks of Nifty 50 and Nifty next 50
        :return:
        """
        for i, symbol in enumerate(self._get_stock_symbols()):
            stock_history = self._get_history(symbol)
            self.stocks_info_list.append(stock_history)


class MovingAverageStrategy(StockScanner):
    """This Class implement EMA Strategy to get all stocks crossing given day EMA
    """
    def __init__(self, **kwargs):
        super(MovingAverageStrategy, self).__init__(**kwargs)
        self.ema_day = kwargs.get('ema_day')
        self.last_days_count = kwargs.get('last_days_count')
        self.stock_crossed_ema_list = []

    def get_stocks_crossing_ema(self):
        for stock in self.stock_crossed_ema_list:
            print(stock['symbol'][0])

    def filter_stocks_for_crossing_ema(self):
        """
        :return:
        """
        close_ema = 'close_%s_ema'%self.ema_day
        for stock_data in self.stocks_info_list:
            stock = StockDataFrame.retype(stock_data)
            _ = stock[close_ema]
            cross_ema_data = [stock_info['open'] > stock_info[close_ema]
                              for stock_date, stock_info in stock.tail(self.last_days_count).iterrows()]
            if all(cross_ema_data):
                self.stock_crossed_ema_list.append(stock_data)


if __name__ == '__main__':
    args = parser.parse_args()
    ema = MovingAverageStrategy(start_date=args.start_date, end_date=args.end_date, ema_day=args.ema_day,
                                last_days_count=args.last_days_count)
    ema.scan_stocks()
    ema.filter_stocks_for_crossing_ema()
    ema.get_stocks_crossing_ema()

