import tensorflow as tf
import numpy as np


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
tf.reset_default_graph()
train_graph = tf.Graph()


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


def build_graph(data):
    with train_graph.as_default():
        vocab_size = len(data)
        # 定义输入、目标和学习率占位符
        input_text = tf.placeholder(tf.int32, [None, None], name="input")
        targets = tf.placeholder(tf.int32, [None, None], name="targets")
        lr = tf.placeholder(tf.float32)

        input_data_shape = tf.shape(input_text)
        # 构建RNN单元并初始化
        # 将一个或多个BasicLSTMCells 叠加在MultiRNNCell中，这里我们使用2层LSTM cell
        cell = tf.contrib.rnn.MultiRNNCell([tf.contrib.rnn.BasicLSTMCell(num_units=rnn_size) for _ in range(2)])
        initial_state = cell.zero_state(input_data_shape[0], tf.float32)
        initial_state = tf.identity(initial_state, name="initial_state")

        # embed_matrix是嵌入矩阵，后面计算相似度(距离)的时候会用到
        embed_matrix = tf.Variable(tf.random_uniform([vocab_size, embed_dim], -1, 1))
        # embed_layer是从嵌入矩阵（查找表）中索引到的向量
        embed_layer = tf.nn.embedding_lookup(embed_matrix, input_text)

        # 使用RNN单元构建RNN
        outputs, state = tf.nn.dynamic_rnn(cell, embed_layer, dtype=tf.float32)
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
