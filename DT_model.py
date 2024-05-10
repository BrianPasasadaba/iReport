import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

def train_decision_tree_model(X, y):
    # Train the decision tree model
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    vectorizer = CountVectorizer()
    X_vectorized = vectorizer.fit_transform(X)
    clf = DecisionTreeClassifier()
    clf.fit(X_vectorized, y_encoded)
    return clf, vectorizer, label_encoder

def predict_category(model, vectorizer, label_encoder, report_details):
    report_vectorized = vectorizer.transform([report_details])
    category_pred = model.predict(report_vectorized)
    predicted_category = label_encoder.inverse_transform(category_pred)[0]
    return predicted_category

# Define category ID mapping
category_id_map = {
    'Medical Emergency': 1,
    'Vehicular Accident': 2,
    'Other Emergency': 3
}
