import tensorflow as tf

if __name__ == '__main__':
    x = tf.Variable(3, name="x")
    y = tf.Variable(4, name="y")
    f = x * x * y + y + 2

    init = tf.compat.v1.global_variables_initializer()
    with tf.compat.v1.Session() as sess:
        result = f()
        print(result)
