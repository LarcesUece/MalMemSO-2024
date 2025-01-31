from . import db


class File(db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
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

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "platform": self.platform,
            "received_at": self.received_at,
            "processing_started_at": self.processing_started_at,
            "processing_finished_at": self.processing_finished_at,
            "malware_detected": self.malware_detected,
            "created_at": self.created_at,
        }


class Model(db.Model):
    __tablename__ = "models"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    algorithm = db.Column(
        "model_algorithm",
        db.Enum("cart", "knn", "mlp", "rf", "svm", name="model_algorithm"),
        nullable=False,
    )
    pickle = db.Column(db.PickleType, nullable=False)
    train_accuracy = db.Column(db.Float, nullable=False)
    train_precision = db.Column(db.Float, nullable=False)
    train_recall = db.Column(db.Float, nullable=False)
    train_f1 = db.Column(db.Float, nullable=False)
    train_init_time = db.Column(db.DateTime, nullable=False)
    train_end_time = db.Column(db.DateTime, nullable=False)
    train_duration = db.Column(db.Interval, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "algorithm": self.algorithm,
            "pickle": self.pickle,
            "train_accuracy": self.train_accuracy,
            "train_precision": self.train_precision,
            "train_recall": self.train_recall,
            "train_f1": self.train_f1,
            "train_init_time": self.train_init_time,
            "train_end_time": self.train_end_time,
            "train_duration": self.train_duration,
            "created_at": self.created_at,
        }


class Analysis(db.Model):
    __tablename__ = "analyses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    initial_data = db.Column(db.Boolean, nullable=False, default=False)
    file_id = db.Column(db.Integer, db.ForeignKey("files.id"), nullable=True)
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
        "analysis_file_class",
        db.Enum("malware", "benign", "undefined", name="analysis_file_class"),
        nullable=False,
        default="undefined",
    )
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "initial_data": self.initial_data,
            "file_id": self.file_id,
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
