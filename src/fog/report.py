from math import isinf, isnan
from os.path import exists
from pandas import DataFrame, read_csv
from uuid import uuid4

from app import app


def create_report_file():
    report_file = app.config.get("REPORT_FILE")

    if not exists(report_file):
        df = DataFrame(
            columns=[
                "dump_id",
                "platform",
                "received_at",
                "processing_started_at",
                "processing_finished_at",
                "malware_detected",
                "status",
                "message",
            ]
        )

        df.to_csv(report_file, index=False)


def update_report(
    dump_id,
    platform=None,
    received_at=None,
    processing_started_at=None,
    processing_finished_at=None,
    malware_detected=None,
    status=None,
    message=None,
):
    report_file = app.config.get("REPORT_FILE")
    df = read_csv(report_file)

    if dump_id in df["dump_id"].values:
        if platform:
            df.loc[df["dump_id"] == dump_id, "platform"] = platform
        if received_at:
            df.loc[df["dump_id"] == dump_id, "received_at"] = received_at
        if processing_started_at:
            df.loc[df["dump_id"] == dump_id, "processing_started_at"] = (
                processing_started_at
            )
        if processing_finished_at:
            df.loc[df["dump_id"] == dump_id, "processing_finished_at"] = (
                processing_finished_at
            )
        if malware_detected:
            df.loc[df["dump_id"] == dump_id, "malware_detected"] = malware_detected
        if status:
            df.loc[df["dump_id"] == dump_id, "status"] = status
        if message:
            df.loc[df["dump_id"] == dump_id, "message"]
    else:
        new_row = {
            "dump_id": dump_id,
            "platform": platform,
            "received_at": received_at,
            "processing_started_at": processing_started_at,
            "processing_finished_at": processing_finished_at,
            "malware_detected": malware_detected,
            "status": status,
            "message": message,
        }
        df.loc[len(df)] = new_row

    df.to_csv(report_file, index=False)


def generate_dump_id():
    report_file = app.config.get("REPORT_FILE")

    df = read_csv(report_file)
    existing_dump_ids = df["dump_id"].values
    dump_id = str(uuid4())

    while dump_id in existing_dump_ids:
        dump_id = str(uuid4())

    update_report(dump_id, status="generating_id")

    return dump_id


def get_report(dump_id):
    report_file = app.config.get("REPORT_FILE")
    df = read_csv(report_file)

    if dump_id in df["dump_id"].values:
        report = df[df["dump_id"] == dump_id].to_dict(orient="records")[0]

        for key, value in report.items():
            if isinstance(value, float) and (isnan(value) or isinf(value)):
                report[key] = None

        return report, 200
    else:
        return {"error": "File ID not found."}, 404
