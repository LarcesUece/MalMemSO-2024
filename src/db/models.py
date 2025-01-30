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
    mem_name_extn = db.Column(db.String(255), nullable=False)
    pslist_nproc = db.Column(db.Integer, nullable=False)
    pslist_nppid = db.Column(db.Integer, nullable=False)
    pslist_avg_threads = db.Column(db.Float, nullable=False)
    pslist_nprocs64bit = db.Column(db.Integer, nullable=False)
    pslist_avg_handlers = db.Column(db.Float, nullable=False)
    dlllist_ndlls = db.Column(db.Integer, nullable=False)
    dlllist_avg_dlls_per_proc = db.Column(db.Float, nullable=False)
    handles_nhandles = db.Column(db.Integer, nullable=False)
    handles_avg_handles_per_proc = db.Column(db.Float, nullable=False)
    handles_nport = db.Column(db.Integer, nullable=False)
    handles_nfile = db.Column(db.Integer, nullable=False)
    handles_nevent = db.Column(db.Integer, nullable=False)
    handles_ndesktop = db.Column(db.Integer, nullable=False)
    handles_nkey = db.Column(db.Integer, nullable=False)
    handles_nthread = db.Column(db.Integer, nullable=False)
    handles_ndirectory = db.Column(db.Integer, nullable=False)
    handles_nsemaphore = db.Column(db.Integer, nullable=False)
    handles_ntimer = db.Column(db.Integer, nullable=False)
    handles_nsection = db.Column(db.Integer, nullable=False)
    handles_nmutant = db.Column(db.Integer, nullable=False)
    ldrmodules_not_in_load = db.Column(db.Integer, nullable=False)
    ldrmodules_not_in_init = db.Column(db.Integer, nullable=False)
    ldrmodules_not_in_mem = db.Column(db.Integer, nullable=False)
    ldrmodules_not_in_load_avg = db.Column(db.Float, nullable=False)
    ldrmodules_not_in_init_avg = db.Column(db.Float, nullable=False)
    ldrmodules_not_in_mem_avg = db.Column(db.Float, nullable=False)
    malfind_ninjections = db.Column(db.Integer, nullable=False)
    malfind_commitCharge = db.Column(db.Integer, nullable=False)
    malfind_protection = db.Column(db.Integer, nullable=False)
    malfind_uniqueInjections = db.Column(db.Integer, nullable=False)
    psxview_not_in_pslist = db.Column(db.Integer, nullable=False)
    psxview_not_in_eprocess_pool = db.Column(db.Integer, nullable=False)
    psxview_not_in_ethread_pool = db.Column(db.Integer, nullable=False)
    psxview_not_in_pspcid_list = db.Column(db.Integer, nullable=False)
    psxview_not_in_csrss_handles = db.Column(db.Integer, nullable=False)
    psxview_not_in_session = db.Column(db.Integer, nullable=False)
    psxview_not_in_deskthrd = db.Column(db.Integer, nullable=False)
    psxview_not_in_pslist_false_avg = db.Column(db.Float, nullable=False)
    psxview_not_in_eprocess_pool_false_avg = db.Column(db.Float, nullable=False)
    psxview_not_in_ethread_pool_false_avg = db.Column(db.Float, nullable=False)
    psxview_not_in_pspcid_list_false_avg = db.Column(db.Float, nullable=False)
    psxview_not_in_csrss_handles_false_avg = db.Column(db.Float, nullable=False)
    psxview_not_in_session_false_avg = db.Column(db.Float, nullable=False)
    psxview_not_in_deskthrd_false_avg = db.Column(db.Float, nullable=False)
    modules_nmodules = db.Column(db.Integer, nullable=False)
    svcscan_nservices = db.Column(db.Integer, nullable=False)
    svcscan_kernel_drivers = db.Column(db.Integer, nullable=False)
    svcscan_fs_drivers = db.Column(db.Integer, nullable=False)
    svcscan_process_services = db.Column(db.Integer, nullable=False)
    svcscan_shared_process_services = db.Column(db.Integer, nullable=False)
    svcscan_interactive_process_services = db.Column(db.Integer, nullable=False)
    svcscan_nactive = db.Column(db.Integer, nullable=False)
    callbacks_ncallbacks = db.Column(db.Integer, nullable=False)
    callbacks_nanonymous = db.Column(db.Integer, nullable=False)
    callbacks_ngeneric = db.Column(db.Integer, nullable=False)
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
            "dlllist_avg_dlls_per_proc": self.dlllist_avg_dlls_per_proc,
            "handles_nhandles": self.handles_nhandles,
            "handles_avg_handles_per_proc": self.handles_avg_handles_per_proc,
            "handles_nport": self.handles_nport,
            "handles_nfile": self.handles_nfile,
            "handles_nevent": self.handles_nevent,
            "handles_ndesktop": self.handles_ndesktop,
            "handles_nkey": self.handles_nkey,
            "handles_nthread": self.handles_nthread,
            "handles_ndirectory": self.handles_ndirectory,
            "handles_nsemaphore": self.handles_nsemaphore,
            "handles_ntimer": self.handles_ntimer,
            "handles_nsection": self.handles_nsection,
            "handles_nmutant": self.handles_nmutant,
            "ldrmodules_not_in_load": self.ldrmodules_not_in_load,
            "ldrmodules_not_in_init": self.ldrmodules_not_in_init,
            "ldrmodules_not_in_mem": self.ldrmodules_not_in_mem,
            "ldrmodules_not_in_load_avg": self.ldrmodules_not_in_load_avg,
            "ldrmodules_not_in_init_avg": self.ldrmodules_not_in_init_avg,
            "ldrmodules_not_in_mem_avg": self.ldrmodules_not_in_mem_avg,
            "malfind_ninjections": self.malfind_ninjections,
            "malfind_commitCharge": self.malfind_commitCharge,
            "malfind_protection": self.malfind_protection,
            "malfind_uniqueInjections": self.malfind_uniqueInjections,
            "psxview_not_in_pslist": self.psxview_not_in_pslist,
            "psxview_not_in_eprocess_pool": self.psxview_not_in_eprocess_pool,
            "psxview_not_in_ethread_pool": self.psxview_not_in_ethread_pool,
            "psxview_not_in_pspcid_list": self.psxview_not_in_pspcid_list,
            "psxview_not_in_csrss_handles": self.psxview_not_in_csrss_handles,
            "psxview_not_in_session": self.psxview_not_in_session,
            "psxview_not_in_deskthrd": self.psxview_not_in_deskthrd,
            "psxview_not_in_pslist_false_avg": self.psxview_not_in_pslist_false_avg,
            "psxview_not_in_eprocess_pool_false_avg": self.psxview_not_in_eprocess_pool_false_avg,
            "psxview_not_in_ethread_pool_false_avg": self.psxview_not_in_ethread_pool_false_avg,
            "psxview_not_in_pspcid_list_false_avg": self.psxview_not_in_pspcid_list_false_avg,
            "psxview_not_in_csrss_handles_false_avg": self.psxview_not_in_csrss_handles_false_avg,
            "psxview_not_in_session_false_avg": self.psxview_not_in_session_false_avg,
            "psxview_not_in_deskthrd_false_avg": self.psxview_not_in_deskthrd_false_avg,
            "modules_nmodules": self.modules_nmodules,
            "svcscan_nservices": self.svcscan_nservices,
            "svcscan_kernel_drivers": self.svcscan_kernel_drivers,
            "svcscan_fs_drivers": self.svcscan_fs_drivers,
            "svcscan_process_services": self.svcscan_process_services,
            "svcscan_shared_process_services": self.svcscan_shared_process_services,
            "svcscan_interactive_process_services": self.svcscan_interactive_process_services,
            "svcscan_nactive": self.svcscan_nactive,
            "callbacks_ncallbacks": self.callbacks_ncallbacks,
            "callbacks_nanonymous": self.callbacks_nanonymous,
            "callbacks_ngeneric": self.callbacks_ngeneric,
            "file_class": self.file_class,
            "created_at": self.created_at,
        }
