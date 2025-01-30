from flask import current_app as app, render_template, request, jsonify
from ..db import db
from ..db.models import File


@app.get("/file/")
def list_files():
    sort_by = request.args.get("sort_by", "id")
    order = request.args.get("order", "asc")

    valid_columns = {
        "id",
        "name",
        "status",
        "platform",
        "received_at",
        "processing_started_at",
        "processing_finished_at",
        "malware_detected",
        "created_at",
    }

    if sort_by not in valid_columns:
        sort_by = "id"

    column = getattr(File, sort_by)
    if order == "desc":
        column = column.desc()

    files = File.query.order_by(column).all()

    if not files:
        return jsonify({"message": "No files found."})

    return render_template("file_list.html", files=files, sort_by=sort_by, order=order)


# @app.post("/file/")
# def post_file():
#     data = request.json
#     file = File(**data)
#     db.session.add(file)
#     db.session.commit()
#     return jsonify(file.as_dict())


@app.get("/file/<string:name>")
def post_file(name: str):
    file = File(name=name)
    db.session.add(file)
    db.session.commit()
    return jsonify(file.as_dict())


@app.get("/file/<int:id>")
def get_file(id: int):
    file = File.query.get_or_404(id)
    return jsonify(file.as_dict())


@app.patch("/file/<int:id>")
def patch_file(id: int):
    file = File.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(file, key, value)
    db.session.commit()
    return jsonify(file.as_dict())


@app.delete("/file/<int:id>")
def delete_file(id: int):
    file = File.query.get_or_404(id)
    db.session.delete(file)
    db.session.commit()
    return jsonify({"message": "File deleted."})
