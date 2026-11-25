import numpy as np
import matplotlib.pyplot as plt


from keras import models, layers, optimizers, losses, metrics


import warnings
warnings.filterwarnings("ignore")

def compile_model(model, optimizer, loss, metrics):
    model.compile(
        optimizer=optimizer,
        loss=loss,
        metrics=[metrics]
    )
    
    return model


def fit_model(model,x_train,y_train, validation_size, epochs=100,batch_size=512):
    x_val = x_train[:validation_size] # datos de validación
    partial_x_train = x_train[validation_size:] # datos de entrenamiento
    y_val = y_train[:validation_size]
    partial_y_train = y_train[validation_size:]

    history = model.fit(
        partial_x_train,
        partial_y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(x_val, y_val)
    )
    
    return history

def plot_loss(history,metrics):
    history_dict = history.history
    loss_values = history_dict['loss']
    val_loss_values = history_dict['val_loss']
    acc = history_dict['val_'+metrics]

    epochs = range(1, len(acc) + 1)
    plt.plot(epochs, loss_values, 'b', label='Training loss', color='red')
    plt.plot(epochs, val_loss_values, 'b', label='Validation loss', color='blue')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.show()

def plot_accuracy(history,metrics):
    history_dict = history.history
    acc = history_dict['val_'+metrics]
    val_acc = history_dict[metrics]

    epochs = range(1, len(acc) + 1)
    plt.plot(epochs, acc, 'b', label='Training acc',color='red')
    plt.plot(epochs, val_acc, 'b', label='Validation acc',color='blue')
    plt.title('Training and validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.show

def plot_accuracy_model(model):
    plt.title("Model accuracy")
    plt.xlabel("Epoch / Iteration")
    plt.ylabel("Accuracy magnitude")
    plt.plot(model.history.history["accuracy"])

def plot_loss_model(model):
    plt.title("Model loss")
    plt.xlabel("Epoch / Iteration")
    plt.ylabel("Loss magnitude")
    plt.plot(model.history.history["loss"])
