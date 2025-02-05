import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np

import lottery
from lottery import fetch_and_store
from lottery.pipelines import process_data
from tensorflow.python.framework import ops


def get_batches(int_text, batch_size, seq_length):
    batchCnt = len(int_text) // (batch_size * seq_length)
    int_text_inputs = int_text[:batchCnt * (batch_size * seq_length)]
    int_text_targets = int_text[1:batchCnt * (batch_size * seq_length)+1]

    result_list = []
    x = np.array(int_text_inputs).reshape(1, batch_size, -1)
    y = np.array(int_text_targets).reshape(1, batch_size, -1)

    x_new = np.dsplit(x, batchCnt)
    y_new = np.dsplit(y, batchCnt)

    for ii in range(batchCnt):
        x_list = []
        x_list.append(x_new[ii][0])
        x_list.append(y_new[ii][0])
        result_list.append(x_list)

    return np.array(result_list)

# 训练迭代次数
epochs = 50
# 批次大小
batch_size = 32
# RNN的大小（隐藏节点的维度）
rnn_size = 512
# 嵌入层的维度
embed_dim = 512
# 序列的长度，始终为1
seq_length = 1
# 学习率
learning_rate = 0.01
# 过多少batch以后打印训练信息
show_every_n_batches = 10

save_dir = './save'
ops.reset_default_graph()
train_graph = tf.Graph()

if __name__ == '__main__':
    union_lotto_list = fetch_and_store.fetch()
    CONVERT = lottery.transfer_data.trans_data(union_lotto_list)
    # 处理原始数据,用前一期的X和本期的Y作为关联预测维度
    data, newest_X = process_data(CONVERT, 0)
    with train_graph.as_default():
        vocab_size = len(data)
        # 定义输入、目标和学习率占位符
        input_text = tf.keras.Input(dtype=tf.int32, shape=(), name="input")
        targets = tf.keras.Input(dtype=tf.int32, shape=(), name="targets")
        lr = tf.keras.Input(dtype=tf.float32, shape=())

        input_data_shape = tf.shape(input_text)
        # 构建RNN单元并初始化
        # 将一个或多个BasicLSTMCells 叠加在MultiRNNCell中，这里我们使用2层LSTM cell
        cell = tf.compat.v1.nn.rnn_cell.MultiRNNCell([tf.compat.v1.nn.rnn_cell.BasicLSTMCell(num_units=rnn_size) for _ in range(2)])
        initial_state = cell.zero_state(input_data_shape[0], tf.float32)
        initial_state = tf.identity(initial_state, name="initial_state")

        # embed_matrix是嵌入矩阵，后面计算相似度(距离)的时候会用到
        embed_matrix = tf.Variable(tf.random.uniform([vocab_size, embed_dim], -1, 1))
        # embed_layer是从嵌入矩阵（查找表）中索引到的向量
        embed_layer = tf.nn.embedding_lookup(embed_matrix, input_text)

        # 使用RNN单元构建RNN
        outputs, state = tf.compat.v1.nn.dynamic_rnn(cell, embed_layer, dtype=tf.float32)
        final_state = tf.identity(state, name="final_state")

        logits = tf.layers.dense(outputs, vocab_size)

        probs = tf.nn.softmax(logits, name='probs')

        cost = tf.contrib.seq2seq.sequence_loss(
            logits,
            targets,
            tf.ones([input_data_shape[0], input_data_shape[1]]))

        norm = tf.sqrt(tf.reduce_sum(tf.square(embed_matrix), 1, keep_dims=True))
        normalized_embedding = embed_matrix / norm

        optimizer = tf.train.AdamOptimizer(lr)

        gradients = optimizer.compute_gradients(cost)
        capped_gradients = [(tf.clip_by_value(grad, -1., 1.), var) for grad, var in gradients if
                            grad is not None]  # clip_by_norm
        train_op = optimizer.apply_gradients(capped_gradients)

        correct_pred = tf.equal(tf.argmax(probs, 2),
                                tf.cast(targets, tf.int64))  # logits <--> probs  tf.argmax(targets, 1) <--> targets
        accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32), name='accuracy')
    batches = get_batches(data[:-(batch_size + 1)], batch_size, seq_length)
    test_batches = get_batches(data[-(batch_size + 1):], batch_size, seq_length)
    top_k = 10
    topk_acc_list = []
    topk_acc = 0
    sim_topk_acc_list = []
    sim_topk_acc = 0

    range_k = 5
    floating_median_idx = 0
    floating_median_acc_range_k = 0
    floating_median_acc_range_k_list = []

    floating_median_sim_idx = 0
    floating_median_sim_acc_range_k = 0
    floating_median_sim_acc_range_k_list = []

    losses = {'train': [], 'test': []}
    accuracies = {'accuracy': [], 'topk': [], 'sim_topk': [], 'floating_median_acc_range_k': [],
                  'floating_median_sim_acc_range_k': []}

    with tf.Session(graph=train_graph) as sess:
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        for epoch_i in range(epochs):
            state = sess.run(initial_state, {input_text: batches[0][0]})

            # 训练的迭代，保存训练损失
            for batch_i, (x, y) in enumerate(batches):
                feed = {
                    input_text: x,
                    targets: y,
                    initial_state: state,
                    lr: learning_rate}
                train_loss, state, _ = sess.run([cost, final_state, train_op], feed)  #
                losses['train'].append(train_loss)

                # Show every <show_every_n_batches> batches
                if (epoch_i * len(batches) + batch_i) % show_every_n_batches == 0:
                    print('Epoch {:>3} Batch {:>4}/{}   train_loss = {:.3f}'.format(
                        epoch_i,
                        batch_i,
                        len(batches),
                        train_loss))

            # 使用测试数据的迭代
            acc_list = []
            prev_state = sess.run(initial_state, {input_text: np.array([[1]])})  # test_batches[0][0]
            for batch_i, (x, y) in enumerate(test_batches):
                # Get Prediction
                test_loss, acc, probabilities, prev_state = sess.run(
                    [cost, accuracy, probs, final_state],
                    {input_text: x,
                     targets: y,
                     initial_state: prev_state})  #

                # 保存测试损失和准确率
                acc_list.append(acc)
                losses['test'].append(test_loss)
                accuracies['accuracy'].append(acc)

                print('Epoch {:>3} Batch {:>4}/{}   test_loss = {:.3f}'.format(
                    epoch_i,
                    batch_i,
                    len(test_batches),
                    test_loss))

                # 利用嵌入矩阵和生成的预测计算得到相似度矩阵sim
                valid_embedding = tf.nn.embedding_lookup(normalized_embedding, np.squeeze(probabilities.argmax(2)))
                similarity = tf.matmul(valid_embedding, tf.transpose(normalized_embedding))
                sim = similarity.eval()

                # 保存预测结果的Top K准确率和与预测结果距离最近的Top K准确率
                topk_acc = 0
                sim_topk_acc = 0
                for ii in range(len(probabilities)):

                    nearest = (-sim[ii, :]).argsort()[0:top_k]
                    if y[ii] in nearest:
                        sim_topk_acc += 1

                    if y[ii] in (-probabilities[ii]).argsort()[0][0:top_k]:
                        topk_acc += 1

                topk_acc = topk_acc / len(y)
                topk_acc_list.append(topk_acc)
                accuracies['topk'].append(topk_acc)

                sim_topk_acc = sim_topk_acc / len(y)
                sim_topk_acc_list.append(sim_topk_acc)
                accuracies['sim_topk'].append(sim_topk_acc)

                # 计算真实值在预测值中的距离数据
                realInSim_distance_list = []
                realInPredict_distance_list = []
                for ii in range(len(probabilities)):
                    sim_nearest = (-sim[ii, :]).argsort()
                    idx = list(sim_nearest).index(y[ii])
                    realInSim_distance_list.append(idx)

                    nearest = (-probabilities[ii]).argsort()[0]
                    idx = list(nearest).index(y[ii])
                    realInPredict_distance_list.append(idx)

                print('真实值在预测值中的距离数据：')
                print('max distance : {}'.format(max(realInPredict_distance_list)))
                print('min distance : {}'.format(min(realInPredict_distance_list)))
                print('平均距离 : {}'.format(np.mean(realInPredict_distance_list)))
                print('距离中位数 : {}'.format(np.median(realInPredict_distance_list)))
                print('距离标准差 : {}'.format(np.std(realInPredict_distance_list)))

                print('真实值在预测值相似向量中的距离数据：')
                print('max distance : {}'.format(max(realInSim_distance_list)))
                print('min distance : {}'.format(min(realInSim_distance_list)))
                print('平均距离 : {}'.format(np.mean(realInSim_distance_list)))
                print('距离中位数 : {}'.format(np.median(realInSim_distance_list)))
                print('距离标准差 : {}'.format(np.std(realInSim_distance_list)))
                #             sns.distplot(realInPredict_distance_list, rug=True)  #, hist=False
                # plt.hist(np.log(realInPredict_distance_list), bins=50, color='steelblue', normed=True )

                # 计算以距离中位数为中心，范围K为半径的准确率
                floating_median_sim_idx = int(np.median(realInSim_distance_list))
                floating_median_sim_acc_range_k = 0

                floating_median_idx = int(np.median(realInPredict_distance_list))
                floating_median_acc_range_k = 0
                for ii in range(len(probabilities)):
                    nearest_floating_median = (-probabilities[ii]).argsort()[0][
                                              floating_median_idx - range_k:floating_median_idx + range_k]
                    if y[ii] in nearest_floating_median:
                        floating_median_acc_range_k += 1

                    nearest_floating_median_sim = (-sim[ii, :]).argsort()[
                                                  floating_median_sim_idx - range_k:floating_median_sim_idx + range_k]
                    if y[ii] in nearest_floating_median_sim:
                        floating_median_sim_acc_range_k += 1

                floating_median_acc_range_k = floating_median_acc_range_k / len(y)
                floating_median_acc_range_k_list.append(floating_median_acc_range_k)
                accuracies['floating_median_acc_range_k'].append(floating_median_acc_range_k)

                floating_median_sim_acc_range_k = floating_median_sim_acc_range_k / len(y)
                floating_median_sim_acc_range_k_list.append(floating_median_sim_acc_range_k)
                accuracies['floating_median_sim_acc_range_k'].append(floating_median_sim_acc_range_k)

            print('Epoch {:>3} floating median sim range k accuracy {} '.format(epoch_i, np.mean(
                floating_median_sim_acc_range_k_list)))  #:.3f
            print('Epoch {:>3} floating median range k accuracy {} '.format(epoch_i, np.mean(
                floating_median_acc_range_k_list)))  #:.3f
            print('Epoch {:>3} similar top k accuracy {} '.format(epoch_i, np.mean(sim_topk_acc_list)))  #:.3f
            print('Epoch {:>3} top k accuracy {} '.format(epoch_i, np.mean(topk_acc_list)))  #:.3f
            print('Epoch {:>3} accuracy {} '.format(epoch_i, np.mean(acc_list)))  #:.3f

        # Save Model
        saver.save(sess, save_dir)  # , global_step=epoch_i
        print('Model Trained and Saved')
        embed_mat = sess.run(normalized_embedding)
    sns.distplot(realInSim_distance_list, rug=True)
    sns.distplot(realInPredict_distance_list, rug=True)
    plt.plot(losses['train'], label='Training loss')
    plt.legend()
    _ = plt.ylim()
    plt.show()
    plt.plot(losses['test'], label='Test loss')
    plt.legend()
    _ = plt.ylim()
    plt.show()