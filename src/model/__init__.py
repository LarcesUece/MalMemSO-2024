import pandas as pd

from model import cart

# from model import cart, knn, mlp, rf, svm
import db
import config


def initialize():
    db.create_table(config.MODEL_TABLE, columns=config.MODEL_COLUMNS)
    data = db.fetch_data(config.DATA_TABLE)
    cart.train(data)
    # if not db.table_has_data(config.MODEL_TABLE):
    #     train()


# def train(data: pd.DataFrame = None):
#     if not data:
#         data = db.fetch_data(config.DATA_TABLE)

#     cart.train(data)
#     knn.train(data)
#     mlp.train(data)
#     rf.train(data)
#     svm.train(data)
