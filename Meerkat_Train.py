import pickle
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

data_dict = pickle.load(open('./data_pickle', 'rb'))


data = np.asarray(data_dict['data'])
symbols = np.asarray(data_dict['symbols'])

x_train, x_test, y_train, y_test = train_test_split(data, symbols, test_size=0.2, shuffle=True, stratify=symbols)

model = RandomForestClassifier()

model.fit(x_train, y_train)

y_predict = model.predict(x_test)

score = accuracy_score(y_predict, y_test)

print('Accuracy Rate: {}%'.format(score * 100))
f = open('model.pickle', 'wb')
pickle.dump({'model': model,}, f)
f.close()