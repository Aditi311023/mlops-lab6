import json
import os
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

os.makedirs('app/artifacts', exist_ok=True)

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Model Accuracy: {accuracy:.4f}")

joblib.dump(model, 'app/artifacts/model.pkl')

metrics = {'accuracy': accuracy}
with open('app/artifacts/metrics.json', 'w') as f:
    json.dump(metrics, f)

print("✅ Training complete!")

