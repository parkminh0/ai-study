from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# 1) 데이터: 숫자 4개 -> 품종 3종류
X, y = load_iris(return_X_y=True)

# 2) 훈련용/시험용 분리 — 못 본 데이터로 채점해야 정직한 점수
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# 3) 모델을 만들고 학습
model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X_train, y_train)

# 4) 채점
pred = model.predict(X_test)
print(f"정확도: {accuracy_score(y_test, pred):.1%}")

# 5) 새로운 꽃 한 송이 예측
names = load_iris().target_names
print(names[model.predict([[5.1, 3.5, 1.4, 0.2]])[0]])