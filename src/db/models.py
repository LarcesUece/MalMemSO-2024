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
