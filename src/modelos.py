from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder

def preparar_dados_modelo(df, features, target):
    X = df[features]
    y = df[target]
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test, le

def treinar_modelo_arvore(X_train, y_train, random_state=42):
    clf = DecisionTreeClassifier(random_state=random_state)
    clf.fit(X_train, y_train)
    return clf

def avaliar_modelo(clf, X_test, y_test, le):
    y_pred = clf.predict(X_test)
    report = classification_report(y_test, y_pred, target_names=le.classes_)
    cm = confusion_matrix(y_test, y_pred)
    tree_rules = export_text(clf, feature_names=list(X_test.columns))
    return report, cm, tree_rules
