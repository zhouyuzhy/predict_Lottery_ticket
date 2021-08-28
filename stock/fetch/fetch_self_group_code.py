from futu import *
import pprint


if __name__ == '__main__':
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    data = quote_ctx.get_user_security_group(group_type=UserSecurityGroupType.CUSTOM)
    name = data[1].iloc[3]
    data1 = quote_ctx.get_user_security(name[0])
    results = []
    for i in range(0,len(data1[1])):
        code = data1[1].loc[i]['code']
        name = data1[1].loc[i]['name']
        result = list()
        market = code.split('.')[0]
        code_num = code.split('.')[1]
        market_num = "-1"
        if code == 'HK.800000':
            market_num = "100"
            code_num = 'HSI'
        elif code == 'HK.800700':
            market_num = "124"
            code_num = 'HSTECH'
        elif market == 'HK':
            market_num = '116'
        elif market == 'SH':
            market_num = '1'
        elif market == 'SZ':
            market_num = '0'
        result.append(code_num)
        result.append(name)
        result.append(code)
        result.append(market_num)
        result.append("")
        results.append(result)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(results)
    quote_ctx.close()
