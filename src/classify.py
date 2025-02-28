import pandas as pd


def classify(model, data):
    df = pd.DataFrame(data)
    df.drop(
        columns=["mem_name_extn", "initial_data", "dump_id", "created_at"],
        errors="ignore",
    )
    results = model.predict(data)
    class_map = {0: "benign", 1: "malware"}
    results = [class_map[result] for result in results]
    return results
