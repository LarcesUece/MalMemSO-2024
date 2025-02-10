from flask import current_app as app, request
from datetime import datetime
import os

from .models import Dump
from ..db import db


@app.get("/dump/")
def get_dumps() -> list:
    dumps = Dump.query.all()
    return {"dumps": [dump.as_dict() for dump in dumps]}


@app.get("/dump/count/")
def get_dumps_count() -> dict:
    count = Dump.query.count()
    return {"dumps": count}


@app.get("/dump/<int:id>")
def get_dump(id: int) -> dict:
    dump = Dump.query.get_or_404(id)
    return {"dump": dump.as_dict()}


@app.post("/dump/")
def post_dump() -> dict:
    if "file" not in request.dumps:
        return {"error": "No file part."}, 400

    file = request.files.get("file")
    received_at = datetime.now()

    if file.filename == "":
        return {"error": "No selected dump."}, 400

    if not file.filename.endswith(".zip"):
        return {"error": "Invalid file extension."}, 400

    path = os.path.join(app.config.get("DIR_ZIP"), file.filename)
    file.save(path)

    dump = Dump(
        name=file.filename,
        path=path,
        size=os.path.getsize(path),
        received_at=received_at,
    )
    db.session.add(dump)
    db.session.commit()

    return {"dump": dump.as_dict()}, 201


@app.patch("/dump/<int:id>")
def patch_dump(id: int) -> dict:
    dump = Dump.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(dump, key, value)
    db.session.commit()
    return {"dump": dump.as_dict()}


@app.delete("/dump/<int:id>")
def delete_dump(id: int) -> dict:
    dump = Dump.query.get_or_404(id)
    db.session.delete(dump)
    db.session.commit()
    return "", 204
