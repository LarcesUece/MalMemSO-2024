import pandas as pd

from config import FEATURES_VOLMEMLYZER_V2, FEATURES_VOLMEMLYZER_V2_2024


def load_data(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception:
        print(f"Error while loading data.")
        raise


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    mapping = {
        old: new
        for old, new in zip(FEATURES_VOLMEMLYZER_V2, FEATURES_VOLMEMLYZER_V2_2024)
        if new is not None
    }

    df.rename(columns=mapping, inplace=True)

    for column in ["Category", "Filename"]:
        if column in df.columns:
            df.rename(columns={column: "mem.name_extn"}, inplace=True)

    to_keep = list(mapping.values()) + ["Class", "mem.name_extn"]
    df = df[[col for col in df.columns if col in to_keep]]

    add_class_column(df)
    return df


def add_class_column(df: pd.DataFrame) -> pd.DataFrame:
    if "Class" not in df.columns:
        df["Class"] = ""

    mask = df["Class"] == ""
    df.loc[mask, "Class"] = (
        df.loc[mask, "mem.name_extn"]
        .str.startswith("Benign", na=False)
        .map({True: "Benign", False: "Malware"})
    )

    return df
