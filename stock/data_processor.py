from pandas import DataFrame
import pandas


def concat_last_n_lines(X, n):
    data = X.copy()
    data = data[::-1].reset_index(drop=True)
    for i in range(n):
        # 行数pop掉i+1行，然后与data拼接
        process_rows = i + 1
        data_i = X.copy()
        data_i = data_i[::-1].reset_index(drop=True)
        data_i_to_be_renamed = data_i[process_rows:].reset_index(drop=True)
        data_i_to_be_renamed.pop('Unnamed: 0')
        for index in data_i_to_be_renamed.columns.values:
            data_i_to_be_renamed = data_i_to_be_renamed.rename(columns={index:index+'_'+str(process_rows)})
        data = pandas.concat([data, data_i_to_be_renamed], axis=1, sort=False)
    return data


def concat_n_attrs(attrs, n):
    result = attrs.copy()
    org_attrs = attrs.copy()
    for i in range(n):
        for index in org_attrs:
            result.append(index+'_'+str(i+1))
    return result
