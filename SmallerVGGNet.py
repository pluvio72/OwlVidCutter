from keras.layers import Conv2D, BatchNormalization,MaxPooling2D, Flatten, Dense, Dropout
from keras.models import Sequential
from keras import backend as K

class SmallerVGGNet:
    @staticmethod
    def build(width, height, depth, classes):
        #initlialize model along with input shape to be
        #"channels last" and channels dimension itself
        model = Sequential()
        inputShape = (width, height, depth)
        chanDim = -1

        #if we are using "channels first" update the 
        #input shape and channels dimension
        if K.image_data_format() == "channels_first":
            inputShape = (depth, height, width)
            chanDim = 1

        #CONV -> RELU -> POOL
        model.add(Conv2D(32, (3,3), padding='same', activation='relu', input_shape=inputShape))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(3,3)))
        model.add(Dropout(0.25))

        #(CONV -> RELU) * 2 -> POOL
        model.add(Conv2D(64, (3,3), padding='same', activation='relu'))
        model.add(BatchNormalization(axis=chanDim))
        model.add(Conv2D(64, (3,3), padding='same', activation='relu'))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Dropout(0.25))

        #(CONV -> RELU) * 2 -> POOL 
        model.add(Conv2D(128, (3,3), padding='same', activation='relu'))
        model.add(BatchNormalization(axis=chanDim))
        model.add(Conv2D(128, (3,3), padding='same', activation='relu'))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Dropout(0.25))

        #first and only set of Fully Connected layers (FC -> RELU)
        model.add(Flatten())
        model.add(Dense(1024, activation='relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.5))

        #softmax classifier 
        model.add(Dense(2, activation='softmax'))

        #return the constructed network architeture
        return model
