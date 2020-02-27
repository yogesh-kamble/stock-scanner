from stock_scanner import StockScanner
from stock_scanner import StockDataFrame
from constants import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--start_date', action="store", help="Start Data", type=str)
parser.add_argument('--end_date', action="store", help="end_data", type=str)
parser.add_argument('--index', action="store", help="Provide NSE Index", type=str)


class BollingerBandStrategy(StockScanner):
    """This Class implement BB Strategy to get all stocks crossing mid bb and rsi above 48
    """
    def __init__(self, **kwargs):
        super(BollingerBandStrategy, self).__init__(**kwargs)
        self.sma_day = kwargs.get('sma_day')
        self.last_days_count = kwargs.get('last_days_count')
        self.stock_crossed_sma_list = []

    def get_stocks_crossing_sma(self):
        file_name = 'stock_with_bb_{}.csv'.format(self.index if self.index else NIFTY500)
        with open(file_name, 'w') as f:
            header_list = ','.join(list(self.stock_crossed_sma_list[0]))
            f.write(header_list + '\n')
            for stock in self.stock_crossed_sma_list:
                print(stock['symbol'][0] + ',' + str(stock['close'].tail(1)[0]))
                stock_info = ','.join(str(v) for v in stock.get_values()[-1])
                f.write(stock_info + '\n')

    def is_stock_crossing_midboll(self, stock):
        """
        :param stock:
        :return:
        """
        is_mid_boll_above = False
        try:
            current_close_price = stock['close'].tail(1)[0]
            current_open_price = stock['open'].tail(1)[0]
        except Exception:
            return False
        sma_price = stock['boll'].tail(1)[0]
        rsi_value = stock['rsi_14'].tail(1)[0]

        if current_close_price > sma_price and rsi_value > 48:
            half_percent = sma_price * 4 / 100
            new_sma_price = sma_price + half_percent
            one_percent = sma_price * 1/100
            one_percent_sma_price = sma_price + one_percent
            if current_open_price > current_close_price:
                # Consider Red Candle near mid bollinger
                print("I am near mid bollinger")
                is_mid_boll_above = current_open_price <= new_sma_price and current_close_price <= one_percent_sma_price
            else:
                is_mid_boll_above = current_close_price <= new_sma_price and current_open_price <= one_percent_sma_price

        return is_mid_boll_above

    def is_stock_crossing_midboll_below(self, stock):
        """
        :param stock:
        :return:
        """
        try:
            current_close_price = stock['close'].tail(1)[0]
        except Exception:
            return False
        sma_price = stock['boll'].tail(1)[0]
        rsi_value = stock['rsi_14'].tail(1)[0]

        if current_close_price < sma_price and rsi_value > 48:
            half_percent = sma_price * 1 / 100
            new_sma_price = sma_price - half_percent
            return current_close_price >= new_sma_price

        return False

    def filter_stocks_for_crossing_sma(self):
        """
        :return:
        """
        close_sma = 'boll'
        for stock_data in self.stocks_info_list:
            stock = StockDataFrame.retype(stock_data)
            _ = stock[close_sma]
            _ = stock['rsi_14']
            if self.is_stock_crossing_midboll(stock):
                stock_data['bb_mid'] = 'Above'
                self.stock_crossed_sma_list.append(stock_data)
            if self.is_stock_crossing_midboll_below(stock):
                stock_data['bb_mid'] = 'Below'
                self.stock_crossed_sma_list.append(stock_data)


if __name__ == "__main__":
    args = parser.parse_args()
    sma = BollingerBandStrategy(start_date=args.start_date, end_date=args.end_date, index=args.index)
    sma.scan_stocks()
    sma.filter_stocks_for_crossing_sma()
    sma.get_stocks_crossing_sma()
