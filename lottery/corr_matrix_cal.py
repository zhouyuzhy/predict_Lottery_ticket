import matplotlib.pyplot as plt
from lottery.config import CONVERT


if __name__ == '__main__':
    corr_matrix = CONVERT.corr()
    corrs = corr_matrix['红_1_exist'].sort_values(ascending=False)
    print(corrs)

    CONVERT.plot(kind="scatter", x="红_1_exist", y="红_1_本次遗漏_10", alpha=0.4, c="红_1_本次遗漏_100", cmap=plt.get_cmap("jet"), colorbar=True, )
    plt.legend()
    plt.show()
    # attributes = ['红_1_总次数_10', '红_1_平均遗漏值_10', '红_1_最大遗漏值_10', '红_1_本次遗漏_10', '红_1_上次遗漏_10', '红_1_总次数_30',
    #               '红_1_平均遗漏值_30', '红_1_最大遗漏值_30', '红_1_本次遗漏_30', '红_1_上次遗漏_30', '红_1_总次数_50', '红_1_平均遗漏值_50',
    #               '红_1_最大遗漏值_50', '红_1_本次遗漏_50', '红_1_上次遗漏_50', '红_1_总次数_100', '红_1_平均遗漏值_100', '红_1_最大遗漏值_100',
    #               '红_1_本次遗漏_100', '红_1_上次遗漏_100'
    #               ]
    # for attribute in attributes:
    #     scatter_matrix(CONVERT[['红_1_exist', attribute]], figsize=(12, 8), diagonal='kde')
    #     plt.show()
