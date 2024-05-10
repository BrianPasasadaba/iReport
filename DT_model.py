import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def preprocess_data(data):
    # Remove leading and trailing spaces from the 'Category' column
    data['Category'] = data['Category'].str.strip()
    # Select 'Report Details' as input feature (X) and 'Category' as target variable (y)
    X = data['Report Details']  # Input feature
    y = data['Category']  # Target variable
    return X, y

def train_decision_tree_model(X, y):
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Vectorize the text data
    vectorizer = CountVectorizer()
    X_train_vectorized = vectorizer.fit_transform(X_train)
    
    # Initialize and train DecisionTreeClassifier
    clf = DecisionTreeClassifier()
    clf.fit(X_train_vectorized, y_train)
    
    return clf, vectorizer, X_test, y_test

def predict_category(model, vectorizer, report_details):
    report_vectorized = vectorizer.transform([report_details])
    predicted_category = model.predict(report_vectorized)[0]
    return predicted_category

# Define category ID mapping
category_id_map = {
    'Medical Emergency': 1,
    'Vehicular Accident': 2,
    'Other Emergency': 3
}
