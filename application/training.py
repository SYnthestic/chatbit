import random
import json
import pickle
import numpy as np
import tensorflow as tf
from os.path import exists

import nltk
# Downloading punkt
# nltk.download('punkt')
# Downloading wordnet
# nltk.download('wordnet')

from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import  SGD

lemmatizer = WordNetLemmatizer()

print(exists(r"C:\Users\sam75\OneDrive - Singapore Polytechnic\SP\Y3\Intern\Work\Chatbox\chatbit\application\intents.json"))
# Opens intents
intents = json.loads(open(r'C:\Users\sam75\OneDrive - Singapore Polytechnic\SP\Y3\Intern\Work\Chatbox\chatbit\application\intents.json').read())

words = []
classes = []
documents = []
# Letters to ignore
ignore_letters = ['?', '!', '.', ',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
            
words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

classes = sorted(set(classes))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
outputEmpty = [0] * len(classes)

for document in documents:
    bag = []
    wordPatterns = document[0]
    wordPatterns = [lemmatizer.lemmatize(word.lower()) for word in wordPatterns]
    for word in words:
        bag.append(1) if word in wordPatterns else bag.append(0)

    outputRow = list(outputEmpty)
    outputRow[classes.index(document[1])] = 1
    training.append(bag + outputRow)




    
# Randomly shuffle stuff
random.shuffle(training)
for n in range(len(training)):
    print(len(training[n]))
    print(training[n])
training = np.array(training)

# Define X and y train
X_train = training[:, :len(words)]
y_train = training[:, len(words):]

# Initialize model
model = Sequential()

# Layer 1
model.add(tf.keras.layers.Dense(256, input_shape=(len(X_train[0]),), activation = 'relu'))
model.add(tf.keras.layers.Dropout(0.5))

# Layer 2
model.add(tf.keras.layers.Dense(128, activation = 'relu'))
model.add(tf.keras.layers.Dropout(0.5))


# Final Layer
model.add(tf.keras.layers.Dense(len(y_train[0]), activation='softmax'))

sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Fit model to data
model.fit(X_train, y_train, epochs=200, batch_size=5, verbose=1)
# Save model
model.save('chatbot_model.h5')
print('Done')
