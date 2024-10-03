from sklearn.metrics import accuracy_score, precision_score
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import numpy as np
from collections import Counter
from pathlib import Path
import tensorflow as  tf
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder

script_location = Path(__file__).absolute().parent
def loadData(file):
    file_path = script_location / file
    with open(file_path, 'r', encoding="utf8") as f:
        data = f.readlines()
    result = []
    for d in data:
        d = d.strip()
        if (len(d) > 0):
            result.append(d)
    return result
# Load preprocessed text data
bad_requests = loadData('anomalousRequestTest.txt')
good_requests = loadData('normalRequestTraining.txt')

# Combine data
all_requests = bad_requests + good_requests

# Create labels
yBad = [1] * len(bad_requests)
yGood = [0] * len(good_requests)
y = yBad + yGood

# TF-IDF vectorization
vectorizer = TfidfVectorizer(min_df=0.0, analyzer="char", sublinear_tf=True, ngram_range=(3, 3))
X = vectorizer.fit_transform(all_requests)

# Convert TF-IDF vectors to sequences of word indices
X_indices = []
for tfidf_vector in X:
    word_indices = np.nonzero(tfidf_vector)[1]  # Extract non-zero indices
    X_indices.append(word_indices)

# Pad sequences to the same length
max_length = max(len(seq) for seq in X_indices)
X_padded = tf.keras.preprocessing.sequence.pad_sequences(X_indices, maxlen=max_length)

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_padded, y, test_size=0.2, random_state=21)
# Load ground truth labels (y_test) and convert them to a list of strings
# Assuming y_test is a numpy array, you can convert it to a list of strings using astype(str)
y_test_labels = [str(label) for label in y_test]

# Read predicted labels from the majority voting results file
predicted_labels = []
with open('majority_vote_results.txt', 'r') as file:
    for line in file:
        if "Sample" in line:
            prediction = line.strip().split(": ")[1]
            predicted_labels.append(prediction)

# Calculate accuracy and precision
label_encoder = LabelEncoder()
y_test_encoded = label_encoder.fit_transform(y_test)
y_pred_encoded = label_encoder.fit_transform(predicted_labels)


precision = precision_score(y_test_encoded, y_pred_encoded, average='weighted')


print("Precision:", precision)