import numpy as np
from scipy.sparse import csr_matrix

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

input_file = 'C:/Users/DELL/music-top-recommend/data/samples.data'


def load_data():
    # 由于在计算过程用到矩阵计算，这里我们需要根据我们的数据设置行，列，和训练的数据准备
    # 标签列表
    target_list = []
    # 行数列表
    fea_row_list = []
    # 特征列表
    fea_col_list = []
    # 分数列表
    data_list = []
    # 设置行号计数器
    row_idx = 0
    max_col = 0

    with open(input_file, 'r', encoding='UTF-8') as fd:
        for line in fd:
            ss = line.strip().split('\001')
            # 标签
            label = ss[0]
            # 特征
            fea = ss[1:]

            # 将标签放入标签列表中
            target_list.append(int(label))

            # 开始循环处理特征：
            for fea_score in fea:
                sss = fea_score.strip().split(':')
                if len(sss) != 2:
                    continue
                feature, score = sss
                # 增加行
                fea_row_list.append(row_idx)
                # 增加列
                fea_col_list.append(int(feature))
                # 填充分数
                data_list.append(float(score))
                if int(feature) > max_col:
                    max_col = int(feature)
            row_idx += 1
    row = np.array(fea_row_list)
    col = np.array(fea_col_list)
    data = np.array(data_list)
    fea_datasets = csr_matrix((data, (row, col)), shape=(row_idx, max_col + 1))
    x_train, x_test, y_train, y_test = train_test_split(fea_datasets, target_list, test_size=0.2, random_state=0)
    return x_train, x_test, y_train, y_test


def main():
    x_train, x_test, y_train, y_test = load_data()
    # 用L2正则话防止过拟合
    model = LogisticRegression(penalty='l2')
    # 模型训练
    model.fit(x_train, y_train)

    ff_w = open('C:/Users/DELL/music-top-recommend/data/model.w', 'w', encoding='UTF-8')
    ff_b = open('C:/Users/DELL/music-top-recommend/data/model.b', 'w', encoding='UTF-8')

    # 写入训练出来的W
    for w_list in model.coef_:
        for w in w_list:
            ff_w.write(','.join(["w:", str(w)]))
            ff_w.write('\n')
            # print >> ff_w, "w: ", w
    # 写入训练出来的B
    for b in model.intercept_:
        ff_b.write(','.join(["b:", str(b)]))
        ff_b.write('\n')
        # print >> ff_b, "b: ", b
    print("precision: ", model.score(x_test, y_test))
    print("MSE: ", np.mean((model.predict(x_test) - y_test) ** 2))


if __name__ == '__main__':
    main()
