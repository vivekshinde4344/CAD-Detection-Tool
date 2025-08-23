import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load datasets
st = pd.read_csv('Heart_disease_statlog.csv').drop(['ca', 'thal'], axis=1)
cl = pd.read_csv('heart_cleveland_upload.csv').drop(['ca', 'thal'], axis=1)
hn = pd.read_csv('heart.csv')

# Encode categorical columns in 'hn'
le = LabelEncoder()
for col in ['sex', 'cp', 'restecg', 'exang', 'slope']:
    hn[col] = le.fit_transform(hn[col])

# Merge datasets
data = pd.concat([st, cl, hn], axis=0)

# Features and target
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Scale features
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=300, max_depth=20, criterion='entropy', random_state=42)
model.fit(X_train, y_train)

# Save model and scaler
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)


