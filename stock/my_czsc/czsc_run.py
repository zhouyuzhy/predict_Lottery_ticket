import pandas as pd
import traceback
from datetime import datetime
import os
from tqdm import tqdm
from collections import OrderedDict
from czsc import signals, CZSC
from czsc.objects import Signal, Factor, Event, Freq, Operate, RawBar

from stock.fetch import fetch_store


def convert2RawBar(klines):
    rowbars = []
    id = 0
    for kline in klines:
        id = id + 1
        rb = RawBar(kline.code, id, kline.time_key, Freq.D, float(kline.open), float(kline.close), float(kline.high), float(kline.low),
                    float(kline.volume))
        rowbars.append(rb)
    return rowbars


def stocks_dwm_selector(end_date: [str, datetime] = datetime.now().strftime('%Y-%m-%d'), data_path=None):
    """大级别选股（日线&月线&周线）"""
    if not data_path:
        home_path = os.path.expanduser('~')
        data_path = os.path.join(home_path, '.czsc_selector')

    print(f"selector results path: {data_path}")

    # df = ts.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    # records = df.to_dict('records')
    file_results = os.path.join(data_path, f"selector_results_{end_date}.xlsx")

    event = Event(name="选股", operate=Operate.LO, factors=[
        Factor(name="月线KDJ金叉_日线MACD强势", signals_all=[
            # Signal("月线_KDJ状态_任意_金叉_任意_任意_0"),
            Signal('日线_MACD状态_任意_DIFF大于0_DEA大于0_柱子增大_0'),
            Signal('日线_MA5状态_任意_收盘价在MA5上方_任意_任意_0'),
        ]),
        Factor(name="月线KDJ金叉_日线潜在三买", signals_all=[
            # Signal("月线_KDJ状态_任意_金叉_任意_任意_0"),
            Signal('日线_倒0笔_潜在三买_构成中枢_近3K在中枢上沿附近_近7K突破中枢GG_0'),
            Signal('日线_MA5状态_任意_收盘价在MA5上方_任意_任意_0'),
        ]),
        Factor(
            name="月线KDJ金叉_周线三笔强势",
            signals_all=[
                # Signal("月线_KDJ状态_任意_金叉_任意_任意_0"),
                Signal('日线_MA5状态_任意_收盘价在MA5上方_任意_任意_0'),
            ],
            # signals_any=[
            #     Signal('周线_倒1笔_三笔形态_向下不重合_任意_任意_0'),
            #     Signal('周线_倒1笔_三笔形态_向下奔走型_任意_任意_0'),
            #     Signal('周线_倒1笔_三笔形态_向下盘背_任意_任意_0'),
            # ]
        ),
        Factor(name="月线KDJ金叉_周线MACD强势", signals_all=[
            # Signal("月线_KDJ状态_任意_金叉_任意_任意_0"),
            # Signal('周线_MACD状态_任意_DIFF大于0_DEA大于0_柱子增大_0'),
            Signal('日线_MA5状态_任意_收盘价在MA5上方_任意_任意_0'),
        ]),
    ])

    results = []
    signals_res = []
    codes = ['HK.01810']
    for symbol in codes:
        try:
            # k0 = ts.get_kline(symbol, asset='E', freq=Freq.D, start_date="20200101", end_date=end_date)
            # k1 = ts.get_kline(symbol, asset='E', freq=Freq.W, start_date="20100101", end_date=end_date)
            # k2 = ts.get_kline(symbol, asset='E', freq=Freq.M, start_date="20000101", end_date=end_date)
            datas = fetch_store.fetch_stock_datas(symbol, start_date="2021-01-01", end_date=end_date)
            k0 = convert2RawBar(datas)
            c0 = CZSC(k0, get_signals=signals.get_selector_signals)
            # c1 = CZSC(k1, get_signals=signals.get_selector_signals)
            # c2 = CZSC(k2, get_signals=signals.get_selector_signals)

            s = OrderedDict({'code': symbol})
            s.update(c0.signals)
            # s.update(c1.signals)
            # s.update(c2.signals)
            signals_res.append(s)

            m, f = event.is_match(s)
            if m:
                dt_fmt = "%Y%m%d"
                res = {
                    'symbol': symbol,
                    # 'name': s['name'],
                    'reason': f,
                    'end_dt': k0[-1].dt.strftime(dt_fmt)
                }
                results.append(res)
                print(res)
        except:
            print("fail on {}".format(symbol))
            traceback.print_exc()

    df_r = pd.DataFrame(results)
    df_r.to_excel(file_results, index=False)
    print(f"selector results saved into {file_results}")
    return df_r


if __name__ == '__main__':
    stocks_dwm_selector()
