from flask import current_app as app, request
from datetime import datetime
from threading import Thread
import os

from .models import Dump
from .utils import process_dump
from ..db import db


@app.get("/dump/")
def get_dumps() -> list:
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    offset = (page - 1) * limit
    dumps = Dump.query.offset(offset).limit(limit).all()
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
    if "file" not in request.files:
        return {"error": "No file part."}, 400

    file = request.files.get("file")
    received_at = datetime.now()

    if file.filename == "":
        return {"error": "No selected dump."}, 400

    if not file.filename.endswith(".zip"):
        return {"error": "Invalid file extension."}, 400

    name = file.filename.split(".")[0]
    zip_path = os.path.join(app.config.get("DIR_ZIP"), file.filename)
    file.save(zip_path)

    dump = Dump(
        name=name,
        zip_path=zip_path,
        received_at=received_at,
    )
    db.session.add(dump)
    db.session.commit()

    thread = Thread(target=process_dump, args=(dump.id, app._get_current_object()))
    thread.start()

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
