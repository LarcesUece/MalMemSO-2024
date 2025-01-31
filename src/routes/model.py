from flask import current_app as app, request
from ..db import db
from ..db.models import Model
from ..training import train_all


@app.get("/model/")
def list_models() -> list:
    models = Model.query.all()
    return [model.as_dict() for model in models]


@app.get("/model/info/")
def get_models_info() -> dict:
    models = Model.query.all()
    return {"models": len(models)}


@app.get("/model/train/")
def train_models():
    train_all()
    return {"status": "ok"}


@app.post("/model/")
def post_model() -> dict:
    data = request.json
    model = Model(**data)
    db.session.add(model)
    db.session.commit()
    return model.as_dict()


@app.get("/model/<int:id>")
def get_model(id: int) -> dict:
    model = Model.query.get_or_404(id)
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
