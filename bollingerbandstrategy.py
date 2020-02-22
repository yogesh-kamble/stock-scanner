from stock_scanner import StockScanner
from stock_scanner import StockDataFrame
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--start_date', action="store", help="Start Data", type=str)
parser.add_argument('--end_date', action="store", help="end_data", type=str)
parser.add_argument('--sma_day', action="store", help="SMA days", type=int)
parser.add_argument('--last_days_count', action="store", help="Latest days to consider", type=int)


class BollingerBandStrategy(StockScanner):
    """This Class implement EMA Strategy to get all stocks crossing given day EMA
    """
    def __init__(self, **kwargs):
        super(BollingerBandStrategy, self).__init__(**kwargs)
        self.sma_day = kwargs.get('sma_day')
        self.last_days_count = kwargs.get('last_days_count')
        self.stock_crossed_sma_list = []

    def get_stocks_crossing_sma(self):
        with open('stocks_with_bb.csv', 'w') as f:
            f.write('Stock,Price' + '\n')
            for stock in self.stock_crossed_sma_list:
                print(stock['symbol'][0] + ',' + str(stock['close'].tail(1)[0]))
                f.write(stock['symbol'][0] + ',' + str(stock['close'].tail(1)[0]) + '\n')

    def filter_stocks_for_crossing_sma(self):
        """
        :return:
        """
        close_sma = 'close_%s_sma'%self.sma_day
        for stock_data in self.stocks_info_list:
            stock = StockDataFrame.retype(stock_data)
            _ = stock[close_sma]
            current_close_price = stock['close'].tail(1)[0]
            sma_price = stock[close_sma].tail(1)[0]
            if current_close_price > sma_price:
                half_percent = sma_price * 1/100
                new_sma_price = sma_price + half_percent
                if current_close_price <= new_sma_price:
                    self.stock_crossed_sma_list.append(stock_data)


if __name__ == "__main__":
    args = parser.parse_args()
    sma = BollingerBandStrategy(start_date=args.start_date, end_date=args.end_date, sma_day=args.sma_day,
                                last_days_count=args.last_days_count)
    sma.scan_stocks()
    sma.filter_stocks_for_crossing_sma()
    sma.get_stocks_crossing_sma()
