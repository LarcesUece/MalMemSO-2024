import os
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.metrics import average_precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from datetime import datetime
import pickle
import os


mean_data = {"pslist.nproc" : 41.39477097412793,
             "pslist.nppid" : 14.713837121987849,
             "pslist.avg_threads" : 11.341655349935714,
             "pslist.nprocs64bit" : 0.0,
             "pslist.avg_handlers" : 247.5098191021759,
             "dlllist.ndlls" : 1810.8054474708172,
             "dlllist.avg_dlls_per_proc" : 43.707805923039345,
             "handles.nhandles" : 10258.584220765923,
             "handles.avg_handles_per_proc" : 249.56095819728972,
             "handles.nport" : 0.0,
             "handles.nfile" : 899.1195132773569,
             "handles.nevent":3572.4099597242134,
             "handles.ndesktop":44.5291658133661,
             "handles.nkey":774.2806676223634,
             "handles.nthread":928.5100860126971,
             "handles.ndirectory":102.39833777049628,
             "handles.nsemaphore":683.3393235033108,
             "handles.ntimer":130.3278551436958,
             "handles.nsection":290.12746603863746,
             "handles.nmutant":312.5888285889822,
             "ldrmodules.not_in_load":60.830346781350265,
             "ldrmodules.not_in_init":99.94641272441805,
             "ldrmodules.not_in_mem":60.832599494846065,
             "ldrmodules.not_in_load_avg":0.03316972257674586,
             "ldrmodules.not_in_init_avg":0.05522275958324801,
             "ldrmodules.not_in_mem_avg":0.033171317090876506,
             "malfind.ninjections":7.010273738821763,
             "malfind.commitCharge":969.1992286162878,
             "malfind.protection":42.282408355519145,
             "malfind.uniqueInjections":1.7336990238644274,
             "modules.nmodules":137.96146494641272,
             "svcscan.nservices":391.34754932077277,
             "svcscan.kernel_drivers":221.40658065396954,
             "svcscan.fs_drivers":25.996245477506996,
             "svcscan.process_services":25.063417298109087,
             "svcscan.shared_process_services":116.87951395999727,
             "svcscan.nactive" : 121.99554577104239,
             "callbacks.ncallbacks" : 86.90565908935764}

pkl_filename = "svm_model.pkl"
output_file = "output.csv"
loaded_model = pickle.load(open(pkl_filename, 'rb'))
#y_test = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

x = pd.read_csv(output_file)
y_test = x["class"]
x = x[["callbacks.ncallbacks", "dlllist.avg_dllPerProc", "dlllist.ndlls","handles.avgHandles_per_proc", "handles.nTypeDesk","handles.nTypeDir","handles.nTypeEvent","handles.nTypeFile",
            "handles.nHandles","handles.nTypeKey", "handles.nTypeMutant", "handles.nTypePort","handles.nTypeSec", "handles.nTypeSemaph", "handles.nTypeThread", "handles.nTypeTimer",
            "ldrmodules.not_in_init", "ldrmodules.not_in_init_avg", "ldrmodules.not_in_load", "ldrmodules.not_in_load_avg", "ldrmodules.not_in_mem", "ldrmodules.not_in_mem_avg",
            "malfind.commitCharge", "malfind.ninjections", "malfind.protection", "malfind.uniqueInjections", "modules.nmodules", "pslist.avg_handlers", "pslist.avg_threads", "pslist.nppid",
            "pslist.nproc", "pslist.nprocs64bit", "svcscan.Type_FileSys_Driver", "svcscan.Type_Kernel_Driver", "svcscan.State_Run", "svcscan.nServices", "svcscan.Type_Own", "svcscan.Type_Share"]]

x = x.rename(columns={"dlllist.avg_dllPerProc": "dlllist.avg_dlls_per_proc", "handles.avgHandles_per_proc" : "handles.avg_handles_per_proc", "handles.nTypeDesk": "handles.ndesktop",
                       "handles.nTypeDir" : "handles.ndirectory", "handles.nTypeEvent" : "handles.nevent", "handles.nTypeFile" : "handles.nfile", "handles.nHandles" : "handles.nhandles",
                       "handles.nTypeKey" : "handles.nkey", "handles.nTypeMutant" : "handles.nmutant", "handles.nTypePort" : "handles.nport", "handles.nTypeSec" : "handles.nsection",
                       "handles.nTypeSemaph" : "handles.nsemaphore", "handles.nTypeThread" : "handles.nthread", "handles.nTypeTimer" : "handles.ntimer", "svcscan.Type_FileSys_Driver" : "svcscan.fs_drivers",
                       "svcscan.Type_Kernel_Driver" : "svcscan.kernel_drivers", "svcscan.State_Run" : "svcscan.nactive", "svcscan.nServices" : "svcscan.nservices", "svcscan.Type_Own" : "svcscan.process_services",
                       "svcscan.Type_Share" : "svcscan.shared_process_services"})

# Replace Nan of the output with column mean value
x.fillna(mean_data, inplace=True)

# Order columns
x = x.sort_index(axis=1)
init_dt = datetime.now()    
y_pred = loaded_model.predict(x)
end_dt = datetime.now()
diff_dt = end_dt - init_dt
print(diff_dt)

print(accuracy_score(y_test, y_pred))
print(average_precision_score(y_test, y_pred))
print(f1_score(y_test, y_pred))
print(recall_score(y_test, y_pred))

