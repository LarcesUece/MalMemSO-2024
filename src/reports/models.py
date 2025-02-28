from flask import current_app as app

from ..db import db


class Report(db.Model):
    __tablename__ = app.config.get("TABLE_REPORT", "reports")

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    initial_data = db.Column(db.Boolean, nullable=False, default=False)
    dump_id = db.Column(db.Integer, db.ForeignKey("dumps.id"), nullable=True)
    mem_name_extn = db.Column(db.String(255), nullable=True)
    pslist_nproc = db.Column(db.Float, nullable=True)
    pslist_nppid = db.Column(db.Float, nullable=True)
    pslist_avg_threads = db.Column(db.Float, nullable=True)
    pslist_nprocs64bit = db.Column(db.Float, nullable=True)
    pslist_avg_handlers = db.Column(db.Float, nullable=True)
    dlllist_ndlls = db.Column(db.Float, nullable=True)
    dlllist_avg_dllperproc = db.Column(db.Float, nullable=True)
    handles_nhandles = db.Column(db.Float, nullable=True)
    handles_avghandles_per_proc = db.Column(db.Float, nullable=True)
    handles_ntypeport = db.Column(db.Float, nullable=True)
    handles_ntypefile = db.Column(db.Float, nullable=True)
    handles_ntypeevent = db.Column(db.Float, nullable=True)
    handles_ntypedesk = db.Column(db.Float, nullable=True)
    handles_ntypekey = db.Column(db.Float, nullable=True)
    handles_ntypethread = db.Column(db.Float, nullable=True)
    handles_ntypedir = db.Column(db.Float, nullable=True)
    handles_ntypesemaph = db.Column(db.Float, nullable=True)
    handles_ntypetimer = db.Column(db.Float, nullable=True)
    handles_ntypesec = db.Column(db.Float, nullable=True)
    handles_ntypemutant = db.Column(db.Float, nullable=True)
    ldrmodules_not_in_load = db.Column(db.Float, nullable=True)
    ldrmodules_not_in_init = db.Column(db.Float, nullable=True)
    ldrmodules_not_in_mem = db.Column(db.Float, nullable=True)
    ldrmodules_not_in_load_avg = db.Column(db.Float, nullable=True)
    ldrmodules_not_in_init_avg = db.Column(db.Float, nullable=True)
    ldrmodules_not_in_mem_avg = db.Column(db.Float, nullable=True)
    malfind_ninjections = db.Column(db.Float, nullable=True)
    malfind_commitcharge = db.Column(db.Float, nullable=True)
    malfind_protection = db.Column(db.Float, nullable=True)
    malfind_uniqueinjections = db.Column(db.Float, nullable=True)
    modules_nmodules = db.Column(db.Float, nullable=True)
    svcscan_nservices = db.Column(db.Float, nullable=True)
    svcscan_type_kernel_driver = db.Column(db.Float, nullable=True)
    svcscan_type_filesys_driver = db.Column(db.Float, nullable=True)
    svcscan_type_own = db.Column(db.Float, nullable=True)
    svcscan_type_share = db.Column(db.Float, nullable=True)
    svcscan_state_run = db.Column(db.Float, nullable=True)
    callbacks_ncallbacks = db.Column(db.Float, nullable=True)
    file_class = db.Column(
        "report_file_class",
        db.Enum("malware", "benign", "undefined", name="report_file_class"),
        nullable=False,
        default="undefined",
    )
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "initial_data": self.initial_data,
            "dump_id": self.dump_id,
            "mem_name_extn": self.mem_name_extn,
            "pslist_nproc": self.pslist_nproc,
            "pslist_nppid": self.pslist_nppid,
            "pslist_avg_threads": self.pslist_avg_threads,
            "pslist_nprocs64bit": self.pslist_nprocs64bit,
            "pslist_avg_handlers": self.pslist_avg_handlers,
            "dlllist_ndlls": self.dlllist_ndlls,
            "dlllist_avg_dllperproc": self.dlllist_avg_dllperproc,
            "handles_nhandles": self.handles_nhandles,
            "handles_avghandles_per_proc": self.handles_avghandles_per_proc,
            "handles_ntypeport": self.handles_ntypeport,
            "handles_ntypefile": self.handles_ntypefile,
            "handles_ntypeevent": self.handles_ntypeevent,
            "handles_ntypedesk": self.handles_ntypedesk,
            "handles_ntypekey": self.handles_ntypekey,
            "handles_ntypethread": self.handles_ntypethread,
            "handles_ntypedir": self.handles_ntypedir,
            "handles_ntypesemaph": self.handles_ntypesemaph,
            "handles_ntypetimer": self.handles_ntypetimer,
            "handles_ntypesec": self.handles_ntypesec,
            "handles_ntypemutant": self.handles_ntypemutant,
            "ldrmodules_not_in_load": self.ldrmodules_not_in_load,
            "ldrmodules_not_in_init": self.ldrmodules_not_in_init,
            "ldrmodules_not_in_mem": self.ldrmodules_not_in_mem,
            "ldrmodules_not_in_load_avg": self.ldrmodules_not_in_load_avg,
            "ldrmodules_not_in_init_avg": self.ldrmodules_not_in_init_avg,
            "ldrmodules_not_in_mem_avg": self.ldrmodules_not_in_mem_avg,
            "malfind_ninjections": self.malfind_ninjections,
            "malfind_commitcharge": self.malfind_commitcharge,
            "malfind_protection": self.malfind_protection,
            "malfind_uniqueinjections": self.malfind_uniqueinjections,
            "modules_nmodules": self.modules_nmodules,
            "svcscan_nservices": self.svcscan_nservices,
            "svcscan_type_kernel_driver": self.svcscan_type_kernel_driver,
            "svcscan_type_filesys_driver": self.svcscan_type_filesys_driver,
            "svcscan_type_own": self.svcscan_type_own,
            "svcscan_type_share": self.svcscan_type_share,
            "svcscan_state_run": self.svcscan_state_run,
            "callbacks_ncallbacks": self.callbacks_ncallbacks,
            "file_class": self.file_class,
            "created_at": self.created_at,
        }
