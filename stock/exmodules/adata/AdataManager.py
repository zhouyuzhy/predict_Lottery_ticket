import adata

if __name__ == '__main__':
    res_df = adata.stock.market.get_market(stock_code='000001', k_type=30, start_date='2024-08-01')
    print(res_df['trade_time', 'close'])