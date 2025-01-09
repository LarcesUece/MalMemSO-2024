from .. import model


def test_initialize():
    model.initialize()
    assert model.db.table_has_data(model.config.MODEL_TABLE)


def test_create_model():
    test_model = model.create_model("cart")
    assert isinstance(test_model, model.DecisionTreeClassifier)
    test_model = model.create_model("knn")
    assert isinstance(test_model, model.KNeighborsClassifier)
    test_model = model.create_model("mlp")
    assert isinstance(test_model, model.MLPClassifier)
    test_model = model.create_model("rf")
    assert isinstance(test_model, model.RandomForestClassifier)
    test_model = model.create_model("svm")
    assert isinstance(test_model, model.SVC)
    try:
        model.create_model("invalid")
    except ValueError:
        assert True
