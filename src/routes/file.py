from flask import current_app as app, render_template, request
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

    return render_template("file_list.html", files=files, sort_by=sort_by, order=order)


@app.get("/file/<string:name>")
def post_file(name: str):
    file = File(name=name)
    db.session.add(file)
    db.session.commit()
    return "Post file."


@app.get("/file/<int:id>")
def get_file(id: int):
    return f"Get file {id}."


@app.patch("/file/<int:id>")
def patch_file(id: int):
    return f"Patch file {id}."


@app.delete("/file/<int:id>")
def delete_file(id: int):
    return f"Delete file {id}."
