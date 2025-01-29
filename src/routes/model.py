from flask import current_app as app


@app.get("/model/")
def list_models():
    return "List models."


@app.post("/model/")
def post_model():
    return "Post model."


@app.get("/model/<int:id>")
def get_model(id: int):
    return f"Get model {id}."


@app.patch("/model/<int:id>")
def patch_model(id: int):
    return f"Patch model {id}."


@app.delete("/model/<int:id>")
def delete_model(id: int):
    return f"Delete model {id}."
