import datetime
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import where
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score


def import_data(which):
    df = pd.read_csv('data/csv/training_queries_{}_2.csv'.format(which),
                     sep=";")
    df = df.sample(frac=1).reset_index(drop=True)

    df.pop("id")
    y = df.pop(which)
    output_len = len(list(set(y)))

    print("{} Shape: ".format(which), df.shape)
    print("Train Stations Number: ", output_len)

    return (df, y, output_len)


def define_model(row, col, name, output):
    model = tf.keras.Sequential(
        [
            # tf.keras.layers.Dense(
            #     output * 20, activation="relu", name="01_Dense_Input"),
            # tf.keras.layers.Dropout(0.7, name="01_Dropout"),
            # tf.keras.layers.Dense(
            #     output * 20, activation="relu", name="02_Dense_Input"),
            # tf.keras.layers.Dropout(0.6, name="02_Dropout"),
            # tf.keras.layers.Conv2D(
            #     output, (32, 32), activation="relu", name="01_CNN"),
            # tf.keras.layers.MaxPooling2D(name="01_MaxPool"),
            # tf.keras.layers.Conv2D(
            #     output * 2, (32, 32), activation="relu", name="02_CNN"),
            # tf.keras.layers.MaxPooling2D(name="02_MaxPool"),
            # tf.keras.layers.Dropout(0.6, name="02_Dropout"),
            tf.keras.layers.Dense(
                output * 4, activation="relu", name="05_Dense"),
            tf.keras.layers.Dropout(0.4, name="05_Dropout"),
            tf.keras.layers.Dense(
                output * 3, activation="relu", name="06_Dense"),
            tf.keras.layers.Dropout(0.2, name="06_Dropout"),
            tf.keras.layers.Dense(
                output * 2, activation="relu", name="07_Dense"),
            tf.keras.layers.Dense(
                output, activation='softmax', name="08_Dense_Output")
        ],
        name=name)

    model.compile(optimizer="adam",
                  loss=tf.keras.losses.CategoricalCrossentropy(),
                  metrics=["accuracy"])
    model.build(input_shape=(row, col))

    model.summary()

    return model


def split_data(df, y):
    '''
    Splits the dataset into training (80%), validation (10%) and testing (10%)
    '''
    first_index = int(df.shape[0] * 0.8)
    second_index = int(df.shape[0] * 0.1)
    sum = first_index + second_index
    third_index = second_index * -1

    train_x = df[:][:first_index]
    val_x = df[:][first_index:sum]
    test_x = df[:][third_index:]
    test_x = test_x[:-1]
    print("Train Set Data:", train_x.shape)
    print("Validation Set Data:", val_x.shape)
    print("Test Set Data:", test_x.shape)

    train_y = y[:][:first_index]
    val_y = y[:][first_index:sum]
    test_y = y[:][third_index:]
    test_y = test_y[:-1]
    print("Train Set Label:", train_y.shape)
    print("Validation Set Label:", val_y.shape)
    print("Test Set Label:", test_y.shape)

    return train_x, val_x, test_x, train_y, val_y, test_y


def train(model, train_x, train_y, val_x, val_y, epochs, batch_size):
    log_dir = "logs/fit/" + datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir,
                                                          histogram_freq=1)
    lr_reduce = tf.keras.callbacks.ReduceLROnPlateau(monitor="val_loss",
                                                     factor=0.3,
                                                     patience=2,
                                                     verbose=2,
                                                     mode="max")

    train_y = tf.one_hot(train_y, depth=818)
    val_y = tf.one_hot(val_y, depth=818)
    history = model.fit(x=train_x.values,
                        y=train_y,
                        validation_data=(val_x, val_y),
                        epochs=epochs,
                        batch_size=batch_size,
                        callbacks=[lr_reduce, tensorboard_callback])
    model.save("./model/test_01")

    return history, model


def metrics(model, history, test_x, test_y, epochs, batch_size):
    '''
    Calculates some training metrics and saves the model to a folder
    '''
    metrics = history.history
    plt.plot(history.epoch, metrics['loss'], metrics['val_loss'])
    plt.legend(['loss', 'val_loss'])
    plt.show()

    print(test_x.values)

    res = model.predict(test_x.values)
    predictions = []
    for pred in res:
        tmp = where(pred < 0.5, 0, 1)
        predictions.append(tmp.numpy().tolist()[0])
    print(predictions)

    acc = accuracy_score(test_y, np.round(res)) * 100

    model_name = ("./saved_models/" + str(epochs) + "_adam_b" +
                  str(batch_size) + "_a" + str(int(acc)) + "_01")

    conf = input("Do you wish to save this model ? (y/n) ")
    if conf == "y":
        model.save(model_name + "/model")

        print("Model {} saved.".format(model_name.split("/")[2]))

    else:
        conf = input(
            "Everything will be lost. Do you wish to save this model ? (y/n) ")
        if conf != "n":
            model.save(model_name + "/model")

            print("Model {} saved.".format(model_name.split("/")[2]))

    return model_name


if __name__ == "__main__":
    print("START: ")
    print("IMPORT DATA")
    (df_start, start, start_output_len) = import_data("start")

    print("SPLIT DATA")
    start_train_x, start_val_x, start_test_x, start_train_y, start_val_y, start_test_y = split_data(
        df_start, start)

    print("IMPORT MODEL")
    start_model = define_model(df_start.shape[0], len(df_start.columns),
                               "Start_Station_MLP", start_output_len)

    print("TRAIN")
    start_history, start_model = train(start_model, start_train_x,
                                       start_train_y, start_val_x, start_val_y,
                                       10, 64)

    # print("METRICS")
    # start_model_name = metrics(start_model, start_history, start_test_x,
    #                            start_test_y, 10, 64)

    # print("\nEND: ")
    # (df_end, end, end_output_len) = import_data("end")
    # end_model = define_model(df_end.shape[0], len(df_end.columns),
    #                          "End_Station_MLP", end_output_len)

    # print("\nEND: ")
    # end_train_x, end_val_x, end_test_x, end_train_y, end_val_y, end_test_y = split_data(
    #     df_end, end)

    # print("\nEND: ")
    # end_history, end_model = train(end_model, end_train_x, end_train_y, end_val_x,
    #                                end_val_y, 10, 64)
    # print("\END: ")
    # end_model_name = metrics(end_model, end_history, end_test_x, end_test_y, 10,
    #                          64)
