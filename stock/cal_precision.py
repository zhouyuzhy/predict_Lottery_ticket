import stock.futu_history_k as futu_history_k
import pandas

if __name__ == '__main__':
    results = pandas.DataFrame()
    for code in futu_history_k.STOCK_CODES:
        result = {}
        datas = pandas.read_csv(code + '_predict.csv')
        incr_same_count = len(datas[(datas['incr_by_close_open'] >= 0.5) & (datas['incr'] >= 0.5)])
        incr_correct_count = len(datas[(datas['incr_by_close_open'] >= 0.5) & (datas['incr'] >= 0.5) & (
                    datas['correct_by_close_open'] == 1) & (datas['correct'] == 1)])
        if incr_same_count>0:
            result['incr_same'] = round(incr_correct_count / incr_same_count, 2)

        drop_same_count = len(datas[(datas['incr_by_close_open'] < 0.5) & (datas['incr'] < 0.5)])
        drop_correct_count = len(datas[(datas['incr_by_close_open'] < 0.5) & (datas['incr'] < 0.5) & (
                datas['correct_by_close_open'] == 1) & (datas['correct'] == 1)])
        result['drop_same'] = round(drop_correct_count / drop_same_count, 2)
        for t in [('incr_by_close_open', 'correct_by_close_open'), ('incr', 'correct')]:
            incr_key = t[0]
            correct_key = t[1]
            total_precision = 0
            total_predict_count = 0
            total_predict_right_count = 0
            incr_predict_count = len(datas[datas[incr_key] >= 0.5])
            incr_predict_right_count = len(datas[(datas[correct_key] == 1) & (datas[incr_key] >= 0.5)])
            print(code, incr_key, incr_predict_count, incr_predict_right_count)
            if incr_predict_count > 0:
                result['incr_' + incr_key] = round(incr_predict_right_count / incr_predict_count, 2)

            drop_predict_count = len(datas[datas[incr_key] < 0.5])
            drop_predict_right_count = len(datas[(datas[correct_key] == 1) & (datas[incr_key] < 0.5)])
            if drop_predict_count > 0:
                result['drop_' + incr_key] = round(drop_predict_right_count / drop_predict_count, 2)

            result['code'] = code
            print(result)
        results = results.append(result, ignore_index=True)
        print(results)
    results.to_csv('precision.csv')
