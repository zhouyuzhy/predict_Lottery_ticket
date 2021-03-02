from abc import ABCMeta, abstractmethod
from futu import *
from pandas import DataFrame
from datetime import datetime


class IDataStream:
    __metaclass__ = ABCMeta

    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def fetch_history(self, code, start, end): raise NotImplementedError

    @abstractmethod
    def fetch_cur(self, code, num): raise NotImplementedError

    @abstractmethod
    def subscribe_k_handle(self, code, handler): raise NotImplementedError


class BaseDataStream(IDataStream):

    def __init__(self, quote_ctx=None, ktype=KLType.K_DAY):
        if self.quote_ctx is None:
            self.quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
        else:
            self.quote_ctx = quote_ctx
        self.ktype = ktype

    def fetch_history(self, code, start, end, use_cache_first=False):
        ktype = self.ktype
        today = datetime.now().strftime('%Y-%m-%d')
        cache_path = 'data/' + code + '_' + ktype + '_' + today + '.csv'
        if use_cache_first and os.path.exists(cache_path):
            return pd.read_csv(cache_path)
        max_count = 1000
        quote_ctx = self.quote_ctx
        data_list = pd.DataFrame()
        ret, data, page_req_key = quote_ctx.request_history_kline(code, ktype=ktype, start=start, end=end,
                                                                  max_count=max_count)
        if ret == RET_OK:
            data_list = data
        else:
            print('error:', data)
            raise Exception('unknown error')
        while page_req_key is not None:  # 请求后面的所有结果
            print('*************************************')
            print('fetch page for', ktype)
            ret, data, page_req_key = quote_ctx.request_history_kline(code, ktype=ktype, start=start, end=end,
                                                                      max_count=max_count,
                                                                      page_req_key=page_req_key)  # 请求翻页后的数据
            if ret == RET_OK:
                data_list = data_list.append(data, ignore_index=True)
            else:
                print('error:', data)
                raise Exception('unknown error')
        data_pd = data_list
        data_pd['incr'] = (data_pd['close'] - data_pd['last_close'] > 0).astype(int)
        data_pd.to_csv(cache_path)
        print('code', code, 'fetch history finished!')
        return data_pd

    def fetch_cur(self, code, num):
        quote_ctx = self.quote_ctx
        ktype = self.ktype
        ret_sub, err_message = quote_ctx.subscribe([code], [ktype], subscribe_push=True)
        # 先订阅K 线类型。订阅成功后FutuOpenD将持续收到服务器的推送，False代表暂时不需要推送给脚本
        if ret_sub == RET_OK:  # 订阅成功
            ret, data = quote_ctx.get_cur_kline(code, num, ktype, AuType.QFQ)
            if ret == RET_OK:
                return data
            else:
                print('error:', data)
        else:
            print('subscription failed', err_message)

    def subscribe_k_handle(self, code, handler):
        pass
