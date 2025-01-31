from flask import current_app as app, request
from ..db import db
from ..db.models import File


@app.get("/file/")
def list_files() -> list:
    files = File.query.all()
    return [file.as_dict() for file in files]


@app.get("/file/info/")
def get_files_info() -> dict:
    files = File.query.all()
    return {"files": len(files)}


@app.post("/file/")
def post_file() -> dict:
    data = request.json
    file = File(**data)
    db.session.add(file)
    db.session.commit()
    return file.as_dict()


@app.get("/file/<int:id>")
def get_file(id: int) -> dict:
    file = File.query.get_or_404(id)
    return file.as_dict()


@app.patch("/file/<int:id>")
def patch_file(id: int) -> dict:
    file = File.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(file, key, value)
    db.session.commit()
    return file.as_dict()


@app.delete("/file/<int:id>")
def delete_file(id: int) -> dict:
    file = File.query.get_or_404(id)
    db.session.delete(file)
    db.session.commit()
    return file.as_dict()
