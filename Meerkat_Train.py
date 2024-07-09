import pickle
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# Load data
data_dict = pickle.load(open('./data_pickle', 'rb'))
data = np.asarray(data_dict['data'])
symbols = np.asarray(data_dict['symbols'])

# Encode the labels
label_encoder = LabelEncoder()
symbols_encoded = label_encoder.fit_transform(symbols)

# Split data
x_train, x_test, y_train, y_test = train_test_split(data, symbols_encoded, test_size=0.2, shuffle=True, stratify=symbols_encoded)

# Define the neural network model
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(42, 1)),
    tf.keras.layers.Conv1D(32, kernel_size=3, activation='relu'),
    tf.keras.layers.MaxPooling1D(pool_size=2),
    tf.keras.layers.Conv1D(64, kernel_size=3, activation='relu'),
    tf.keras.layers.MaxPooling1D(pool_size=2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(len(label_encoder.classes_), activation='softmax')
])

# Compile the model
lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
    initial_learning_rate=1e-3,
    decay_steps=10000,
    decay_rate=0.9)
optimizer = tf.keras.optimizers.Adam(learning_rate=lr_schedule)
model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)
model.fit(x_train, y_train, epochs=50, batch_size=32, validation_split=0.2, callbacks=[early_stopping])

# Evaluate the model
y_predict = model.predict(x_test)
y_predict_classes = np.argmax(y_predict, axis=1)

score = accuracy_score(y_test, y_predict_classes)
print('Accuracy Rate: {}%'.format(score * 100))

# Save the model
model.save('model.h5')

# Save the label encoder
with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)
