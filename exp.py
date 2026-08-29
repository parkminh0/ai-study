from sklearn.datasets import load_iris, load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
 
X, y = load_iris(return_X_y=True)
 
print("[실험 1] random_state만 바꿔봤을 때 (iris)")
for seed in [0, 1, 7, 42, 99, 123]:
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=seed)
    m = DecisionTreeClassifier(max_depth=3, random_state=42).fit(Xtr, ytr)
    print(f"  random_state={seed:3d} -> 정확도 {accuracy_score(yte, m.predict(Xte)):.1%}")
 
print("\n[실험 2] 교차검증 (5번 나눠서 평균)")
s = cross_val_score(DecisionTreeClassifier(max_depth=3, random_state=42), X, y, cv=5)
print(f"  각 회차: {[f'{v:.1%}' for v in s]}")
print(f"  평균 {s.mean():.1%} (± {s.std():.1%})")
 
print("\n[실험 3] 어려운 데이터 (유방암 진단, 특성 30개)")
Xc, yc = load_breast_cancer(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(Xc, yc, test_size=0.3, random_state=42)
for d in [1, 3, 10, None]:
    m = DecisionTreeClassifier(max_depth=d, random_state=42).fit(Xtr, ytr)
    tr = accuracy_score(ytr, m.predict(Xtr))
    te = accuracy_score(yte, m.predict(Xte))
    print(f"  max_depth={str(d):>4} -> 훈련 {tr:.1%} / 시험 {te:.1%}  (차이 {tr-te:+.1%})")
 