from flask import current_app as app
from ..db import db


class Dump(db.Model):
    __tablename__ = app.config.get("TABLE_DUMP", "dumps")

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    report_id = db.Column(db.Integer, db.ForeignKey("reports.id"), nullable=True)
    name = db.Column(db.String(255), nullable=False)
    zip_path = db.Column(db.String(512), nullable=False)
    raw_path = db.Column(db.String(512), nullable=True)
    size = db.Column(db.BigInteger, nullable=True)
    status = db.Column(
        "file_status",
        db.Enum("processing", "processed", "failed", "waiting", name="file_status"),
        nullable=False,
        default="waiting",
    )
    platform = db.Column(db.String(255), nullable=True)
    received_at = db.Column(db.DateTime, nullable=True)
    processing_started_at = db.Column(db.DateTime, nullable=True)
    processing_finished_at = db.Column(db.DateTime, nullable=True)
    malware_detected = db.Column(db.Boolean, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "zip_path": self.zip_path,
            "raw_path": self.raw_path,
            "size": self.size,
            "status": self.status,
            "platform": self.platform,
            "received_at": self.received_at,
            "processing_started_at": self.processing_started_at,
            "processing_finished_at": self.processing_finished_at,
            "malware_detected": self.malware_detected,
            "created_at": self.created_at,
        }
