import pickle
import pandas as pd
import seaborn as sns
from sklearn.metrics import confusion_matrix, precision_score


# load the model from disk
loaded_model = pickle.load(open(model, 'rb'))
X_test = pd.read_csv(X_test_path)
y_test = pd.read_csv(y_test_path)

y_test_pred = loaded_model.predict(X_test)
cfm = confusion_matrix(y_test_pred, y_test)
print(precision_score(y_test_pred, y_test))
sns.heatmap(cfm, cmap='YlGnBu', annot=True, fmt='d', linewidths=.5);