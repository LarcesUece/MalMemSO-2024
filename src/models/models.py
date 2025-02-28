from flask import current_app as app

from ..db import db


class Model(db.Model):
    __tablename__ = app.config.get("TABLE_MODEL", "models")

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    algorithm = db.Column(
        "model_algorithm",
        db.Enum("cart", "knn", "mlp", "rf", "svm", name="model_algorithm"),
        nullable=False,
    )
    pickle = db.Column(db.PickleType, nullable=False)
    pickle_name = db.Column(db.String(255), nullable=False)
    train_accuracy = db.Column(db.Float, nullable=False)
    train_precision = db.Column(db.Float, nullable=False)
    train_recall = db.Column(db.Float, nullable=False)
    train_f1 = db.Column(db.Float, nullable=False)
    train_init_time = db.Column(db.DateTime, nullable=False)
    train_end_time = db.Column(db.DateTime, nullable=False)
    train_duration = db.Column(db.Interval, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "algorithm": self.algorithm,
            "pickle_name": self.pickle_name,
            "train_accuracy": self.train_accuracy,
            "train_precision": self.train_precision,
            "train_recall": self.train_recall,
            "train_f1": self.train_f1,
            "train_init_time": self.train_init_time,
            "train_end_time": self.train_end_time,
            "train_duration": self.train_duration.total_seconds(),
            "created_at": self.created_at,
        }
