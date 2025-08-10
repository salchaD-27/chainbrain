# training and saving a Random Forest machine learning model using scikit-learn and pandas
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load your training data
df = pd.read_csv('../data/training_dataset.csv')

# Prepare features and labels
X = df.drop(columns=['label', 'blockNumber'])
y = df['label']

# Train/test split
# Splits data randomly—80% for training, 20% for testing.
# random_state=42 ensures reproducibility of the split.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
# Initializes a Random Forest with 100 trees.
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
# Makes predictions on the test set.
# Prints a classification report:
# Precision: out of all predicted positives, how many are actually positive?
# Recall: out of all actual positives, how many did we predict?
# F1-score: harmonic mean of precision and recall.
# Support: number of occurrences of each class in y_test
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))


# Saves trained model to disk
# loaded (as in FastAPI server) for making real-time predictions
joblib.dump(clf, '../models/rf_model.pkl')