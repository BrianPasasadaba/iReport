from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse import hstack
from nltk.corpus import stopwords
import numpy as np

# Define Tagalog stop words
tagalog_stop_words = ['po', 'sa', 'na', 'ang', 'kami', 'rito', 'dito', 'di', 'ng', 'yung', 'at', 'ay', 'bago', 'din', 'doon', 'habang', 'hanggang', 'hindi', 'iba', 'isa', 'kami', 'kanila', 'kanilang', 'ko', 'kong', 'lahat', 'marami', 'may', 'mayroon', 'mga', 'nagkaroon', 'nakita', 'namin', 'napaka', 'narito', 'nandito', 'ngayon', 'ni', 'nila', 'nilang', 'nito', 'o', 'pa', 'pagkatapos', 'pagtapos', 'pag', 'para', 'pero', 'silang', 'sila', 'wala', 'walang']

# Combine English and Tagalog stop words
stop_words = stopwords.words('english') + tagalog_stop_words

def load_data_and_train_model(report_details):
  """
  Loads data from a CSV file and trains a KMeans model.

  Args:
      data_path (str): The path to the CSV file containing report details.

  Returns:
      tuple: A tuple containing the trained TfidfVectorizer, KMeans model, and report details as a pandas Series.
  """


  # Initialize and fit TF-IDF vectorizer
  clusterVectorizer = TfidfVectorizer(max_features=1000, stop_words=stop_words)
  X_text = clusterVectorizer.fit_transform(report_details)

  # Define and train KMeans model (replace with your desired number of clusters)
  k = 2
  kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=300, n_init=10, random_state=0)
  kmeans.fit(X_text)

  return clusterVectorizer, kmeans

def predict_cluster_and_distance(clusterVectorizer, kmeans, new_report_details):
  """
  Predicts the cluster for a new report detail and calculates the distance to the nearest centroid.

  Args:
      vectorizer (sklearn.feature_extraction.text.TfidfVectorizer): The trained TF-IDF vectorizer.
      kmeans (sklearn.cluster.kmeans): The trained KMeans model.
      new_report_details (str): The new report detail to predict the cluster for.

  Returns:
      tuple: A tuple containing the predicted cluster label and the distance to the nearest centroid.
  """

  # Convert the new report detail to a TF-IDF vector
  new_report_details_vectorized = clusterVectorizer.transform([new_report_details])

  # Predict the cluster label for the new report
  predicted_cluster = kmeans.predict(new_report_details_vectorized)[0]

  # Calculate the distances to all centroids
  distances = kmeans.transform(new_report_details_vectorized)[0]

  # Find the index of the nearest centroid
  nearest_centroid_index = np.argmin(distances)

  # Calculate the distance to the nearest centroid
  distance_to_nearest_centroid = distances[nearest_centroid_index]

  return predicted_cluster, distance_to_nearest_centroid
