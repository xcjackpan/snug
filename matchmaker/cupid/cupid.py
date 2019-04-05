import tensorflow as tf
import numpy as np
import keras.backend as K
from keras.layers import Input, Dense, LeakyReLU
from keras.models import Model
from keras.models import model_from_json
from random import shuffle
import os

float_formatter = lambda x: "%.2f" % x
np.set_printoptions(formatter={'float_kind':float_formatter})


def gen_data_raw(user_info,pref_map, num_layouts, size=1000, var=10):
    average = 1
    high = 10
    data_x = []
    data_y = []
    for _ in range(size):
        for field, val, layout in pref_map:
            x = list(user_info.values())+[np.random.randint(num_layouts)]
            data_x.append(x)
            data_y += [average]
            
    for _ in range(size):
        for field, val, layout in pref_map:
            u = user_info.copy()
            u[field] = val 
            if not isinstance(val, str):
                u[field] += np.random.rand()*var - var/2
            x = list(u.values())+[layout]
            data_x.append(x)
            data_y += [high]
    
    zipped = list(zip(data_x,data_y))
    shuffle(zipped)
    data_x, data_y = zip(*zipped)
    
    return (data_x, data_y)

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def data_clean(x):
    for a in range(len(x)):
        for b in range(len(x[a])):
            e = x[a][b]
            if isinstance(e, int):
                x[a][b] = float(e)
            elif isinstance(e, str):
                if e == '':
                    x[a][b]=0
                elif is_int(e[0]):
                    # date
                    x[a][b]=0
                else:
                    # browser categorical
                    if e == "Chrome":
                        x[a][b] = 0
                    else:
                        x[a][b] = 1
                    
            elif e == None:
                x[a][b] = 0
    return x

def data_normalize(x):
    average = np.sum(x,axis=0)/x.shape[0]
    for a in range(len(x)):
        for b in range(len(x[a])):
            x[a][b] = x[a][b]/(average[b]+0.0001) - 0.5
            
    return x

def gen_data(user_info,pref_map, num_layouts, size=1000, var=10):
    data_x, data_y = gen_data_raw(user_info,pref_map, num_layouts, size, var)

    data_x = data_clean(data_x)
    
    data_x = np.array(data_x)
    data_y = np.array(data_y)
    
    data_x = data_normalize(data_x)
    
    return (data_x, data_y)

def gen_duration_model(input_size):
    inputs = Input(shape=(input_size,))
    
    d = Dense(64, kernel_initializer='normal', activation='tanh')(inputs)
#     d = Dense(64, kernel_initializer='normal', activation='tanh')(d)
#     d = Dense(16, kernel_initializer='normal', activation='tanh')(d)
    d = Dense(1)(d)
    predicted_stay = LeakyReLU(alpha=0.3)(d)
    model = Model(inputs=inputs, outputs=predicted_stay)
    return model


# returns trained default model based on user pref
def build_model(user_info, pref_map, num_class):
    K.clear_session()
    data_x, data_y = gen_data(user_info, pref_map, num_class, 500,0)
    val_x, val_y = gen_data(user_info, pref_map, num_class, 10,0)
    
    model = gen_duration_model(data_x.shape[1])
    model.compile(optimizer='sgd',
                loss='mean_squared_error')
    history = model.fit(data_x, data_y, validation_split=0.33, epochs=7)
    loss = model.evaluate(val_x, val_y)

    # plt.plot(history.history['loss'])
    # plt.plot(history.history['val_loss'])
    # plt.title('model loss')
    # plt.ylabel('loss')
    # plt.xlabel('epoch')
    # plt.legend(['train', 'test'], loc='upper left')
    # plt.show()
    # for i in range(2,7):
    #     print(model.predict(np.array([val_x[i]])), val_y[i])
    # np.round(val_x[0])
    # np.round(val_x[2])

    return (model, loss)

# writes models to disk
def save_model(model, name="temp"):
    model_json = model.to_json()
    mdir = "model_h5"
    os.remove('{}/{}.json'.format(mdir,name))
    os.remove('{}/{}.h5'.format(mdir,name))
    with open("{}/{}.json".format(mdir,name), "w") as json_file:
        json_file.write(model_json)
    # weights to HDF5
    model.save_weights("{}/{}.h5".format(mdir,name))
    print("saved model to disk")

# reads model from disk
def load_model(name="temp"):
    K.clear_session()
    mdir = "model_h5"
    json_file = open('{}/{}.json'.format(mdir,name), 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights
    loaded_model.load_weights('{}/{}.h5'.format(mdir,name))
    loaded_model.compile(optimizer='sgd',
                loss='mean_squared_error')
    print("loaded")
    return loaded_model

def eval_model(model, user_info={}, pref_map={}, num_class=3, data=None):
    val_x, val_y = gen_data(user_info, pref_map, num_class, 10,0)
    # append data to val data, maybe discount auto-gen data
    loss = model.evaluate(val_x, val_y)
    return loss

def clear_session():
    K.clear_session()