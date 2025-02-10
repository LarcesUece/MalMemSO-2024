from flask import current_app as app, request
from threading import Thread
from ..db import db
from .models import Model
from ..training import train_all


@app.get("/model/")
def get_models() -> list:
    models = Model.query.all()
    return {"models": [model.as_dict() for model in models]}


@app.get("/model/count/")
def get_models_count() -> dict:
    count = Model.query.count()
    return {"models": count}


@app.get("/model/<int:id>")
def get_model(id: int) -> dict:
    model = Model.query.get_or_404(id)
    return model.as_dict()


@app.get("/model/train/")
def train_models():
    thread = Thread(target=train_all, args=(app._get_current_object(),))
    thread.start()
    return {"message": "training started"}, 202


@app.post("/model/")
def post_model() -> dict:
    data = request.json
    model = Model(**data)
    db.session.add(model)
    db.session.commit()
    return model.as_dict()


@app.patch("/model/<int:id>")
def patch_model(id: int) -> dict:
    model = Model.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(model, key, value)
    db.session.commit()
    return model.as_dict()


@app.delete("/model/<int:id>")
def delete_model(id: int) -> dict:
    model = Model.query.get_or_404(id)
    db.session.delete(model)
    db.session.commit()
    return model.as_dict()
