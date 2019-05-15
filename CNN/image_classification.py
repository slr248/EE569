
# In[1]:


import tensorflow as tf
import keras
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense,Conv2D,Dropout,Flatten,MaxPooling2D,AveragePooling2D,Reshape
from keras import optimizers


# In[2]:


(x_train,y_train),(x_test,y_test)=tf.keras.datasets.mnist.load_data()


# In[3]:


x_train_neg=255-x_train
x_test_neg=255-x_test


# In[4]:


x_train=x_train.reshape(*x_train.shape,1)
x_test=x_test.reshape(*x_test.shape,1)
x_train_neg=x_train_neg.reshape(*x_train_neg.shape,1)
x_test_neg=x_test_neg.reshape(*x_test_neg.shape,1)


# In[5]:


plt.imshow(x_train_neg[10000,:,:,0],cmap='gray')
x_train.shape


# In[27]:


model=Sequential()
#model.add(Reshape((28,28,1), input_shape=(784,)))
model.add(Conv2D(6,kernel_size=(5,5),strides=(1,1),padding='same',activation='sigmoid',input_shape=(28,28,1)))
model.add(MaxPooling2D(pool_size=(2, 2),strides=(2,2),padding='same'))
model.add(Conv2D(16,kernel_size=(5,5),strides=(1,1),padding='same',activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2),strides=(2,2),padding='same'))

#model.add(Flatten()) # Flattening the 2D arrays for fully connected layers
#model.add(Dense(120,activation='relu'))
#model.add(Dropout(0.2))
model.add(Conv2D(120,kernel_size=(5,5),strides=(1,1),padding='same',activation='relu'))
model.add(Flatten())
model.add(Dense(84, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(10,activation='softmax'))


# In[8]:


model.summary()


# In[28]:


rms=optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=0.0)
sgd = optimizers.SGD(lr=0.001, momentum=0.25)
Adam=optimizers.Adam(lr=0.001)
ada=optimizers.Adagrad(lr=0.001, epsilon=None, decay=0.0)
model.compile(optimizer=ada,
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
history=model.fit(x=x_train,y=y_train, validation_data=(x_test,y_test),epochs=10,batch_size=128)
plt.plot(history.history['acc'])
plt.ylabel('Training accuracy')
plt.xlabel('epoch')
plt.show()


# In[29]:


print("mean acc: {0}".format(np.average(history.history['acc'])))
print("mean test acc: {0}".format(np.average(history.history['val_acc'])))

print("acc variance: {0}".format(np.std(history.history['acc'])**2))
print("Test acc variance: {0}".format(np.std(history.history['val_acc'])**2))


# In[14]:


plt.plot(history.history['val_acc'])
plt.ylabel('Test set accuracy')
plt.xlabel('epoch')
plt.show()


# In[20]:


plt.plot(history.history['loss'])
plt.ylabel('loss')
plt.xlabel('epoch')
plt.show()


# In[19]:


#x_test=x_test.reshape(10000,28,28,1)
scores=model.evaluate(x_test_neg,y_test)
#plt.plot(scores.scores['acc'])
#plt.plot(history.history)
#plt.show()
print("accuracy on negative image test set (%) :{0} %".format(scores[1]*100))
print("loss :{0}".format(scores[0]))


# In[26]:


x_train_neg=255-x_train
plt.imshow(x_train_neg[10000,:,:,0],cmap='gray')


# In[19]:



model.compile(optimizer=Adam,
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
history1=model.fit(x=x_train_neg,y=y_train, epochs=2,batch_size=128)
plt.plot(history1.history['acc'])
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.show()


# In[23]:


x_test_neg=255-x_test
scores=model.evaluate(x_test_neg,y_test)
#plt.plot(scores.scores['acc'])
#plt.plot(history.history)
#plt.show()
print("accuracy on test set (%) :{0} %".format(scores[1]*100))
print("loss :{0}".format(scores[0]))


# In[23]:


x_new_train=np.concatenate((x_train,x_train_neg))
y_new_train=np.concatenate((y_train,y_train))
x_new_test=np.concatenate((x_test,x_test_neg))
y_new_test=np.concatenate((y_test,y_test))


# In[24]:


model=Sequential()

model.add(Conv2D(16,kernel_size=(5,5),strides=(1,1),padding='same',activation='sigmoid',input_shape=(28,28,1)))
model.add(MaxPooling2D(pool_size=(2, 2),strides=(2,2),padding='same'))
model.add(Conv2D(36,kernel_size=(5,5),strides=(1,1),padding='same',activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2),strides=(2,2),padding='same'))


model.add(Conv2D(120,kernel_size=(5,5),strides=(1,1),padding='same',activation='relu'))
model.add(Flatten())
model.add(Dense(84, activation='relu'))

model.add(Dense(42,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10,activation='softmax'))


# In[25]:


rms=optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=0.0)
sgd = optimizers.SGD(lr=0.001, momentum=0.25)
Adam=optimizers.Adam(lr=0.001)
ada=optimizers.Adagrad(lr=0.001, epsilon=None, decay=0.0)
model.compile(optimizer=Adam,
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
history=model.fit(x=x_new_train,y=y_new_train, validation_data=(x_new_test,y_new_test),shuffle=True,epochs=10,batch_size=128)
plt.plot(history.history['acc'])
plt.ylabel('Training accuracy')
plt.xlabel('epoch')
plt.show()


# In[26]:


plt.plot(history.history['val_acc'])
plt.ylabel('Test set accuracy')
plt.xlabel('epoch')
plt.show()


# In[36]:


print("mean validation set accuracy over 10 epochs: {0}".format(np.round(np.average(history.history['val_acc']),4)))

print("accuracy validation set accuracy variance over 10 epochs: {0}".format((np.std(history.history['val_acc'])**2)))


# In[33]:



scores=model.evaluate(x_test,y_test)
print("accuracy on original test set (%) :{0} %".format(scores[1]*100))
print("loss :{0}".format(scores[0]))


# In[34]:


model.summary()
