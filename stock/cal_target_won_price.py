import pandas as pd


if __name__ == '__main__':

    target_price = 260
    now_price = 244
    own_stock_price = [29.5,52]
    own_fund_wan = [21.2,29.6]
    delta = (target_price-now_price)
    own_stock_price_d = pd.DataFrame(own_stock_price)
    fund_d = pd.DataFrame(own_fund_wan)
    print(pd.DataFrame.sum(delta / own_stock_price_d * fund_d)[0] + pd.DataFrame.sum(fund_d))
    # won = delta/s1*p1 + delta/s2*p2+delta/s3*p3+delta/s4*p4
    # print(won)
    # print(won+66)