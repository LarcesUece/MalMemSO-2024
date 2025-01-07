import cart, knn, mlp, rf, svm
from data import fetch_data_from_db
import os


def train():
    data = fetch_data_from_db()
    cart.train(data)
    knn.train(data)
    mlp.train(data)
    rf.train(data)
    svm.train(data)


def save_training_details(details: list):
    table_name = os.getenv("MODEL_TABLE")
