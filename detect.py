import os
import pandas as pd
#from sklearn.metrics import accuracy_score
#from sklearn.metrics import average_precision_score
#from sklearn.metrics import f1_score
#from sklearn.metrics import recall_score
#from datetime import datetime
import pickle
import os
import time

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




def extract_features_from_dump(ip, datetime):

    # windows credentials
    win_user_login = "suporte"
    win_user_passwd = "123456"

    print("mount windows dir")
    # mount Windows Dump Shared Directory
    cmd = "mount -t cifs //" + ip + "/Users/suporte/Documents/Dumps /var/app/dumps/" + ip + " -o username=" + win_user_login + ",password=" + win_user_passwd
    os.system(cmd)
    
    print("copy dump")
    # copy dump to work directory
    cmd = "cp /var/app/dumps/"+ ip + "/" + datetime + ".tar.gz " + "/var/app/dumps/" 
    os.system(cmd)
    #time.sleep(120)

    print("uncompress dump")
    # uncompress dump
    cmd = "tar -xzvf /var/app/dumps/" + datetime + ".tar.gz" 
    os.system(cmd)
    
    print("change dump extension")
    cmd = "mv /var/app/" + datetime + " /var/app/dumps/" + datetime + ".raw"
    os.system(cmd)
  
    print("remove tar gz dump")
    cmd = "rm /var/app/dumps/" + datetime + ".tar.gz"
    os.system(cmd)
    
    #cmd = "mv " + datetime + " /var/app/dumps/" + datetime + ".raw"
    #os.system(cmd)

    #print("Remove Windows Dump")
    # remove windows dump
    #win_dump_path = "/var/app/dumps/" + ip + "/" + datetime

    #if os.path.exists(win_dump_path):
    #    os.remove(win_dump_path)


    print("umount Windows")
    # Unmount Windows Dump Shared Directory
    cmd = "umount /var/app/dumps/" + ip
    os.system(cmd)

    print("extract features")
    # extract features from dump
    cmd = "python3 /var/app/VolMemLyzer/VolMemLyzer-V2.py -f /var/app/dumps/ -o /var/app/dumps/ -V /var/app/volatility3/vol.py"
    os.system(cmd)

    # remove local dump 
    local_dump_path = "/var/app/dumps/" + datetime

    if os.path.exists(local_dump_path):
        os.remove(local_dump_path)

    return

def analysis(ip, datetime):
    extract_features_from_dump(ip, datetime)

    #print("init classification")
    print("load model")
    pkl_filename = "cart_model_v2.pkl"
    pkl = open(pkl_filename, 'rb')
    
    loaded_model = pickle.load(pkl)
    
    print("read features")
    x = pd.read_csv("dumps/output.csv")
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
    print("process data")
    x.fillna(mean_data, inplace=True)

    # Order columns
    x = x.sort_index(axis=1)
    
    print("predict")
    y_pred = loaded_model.predict(x)
    print(y_pred)
    print(y_pred[0])
    if(y_pred[0] == 1):
        print("A malware was found.")  
        return True
    else:
        print("NO malware was found.")
        return False
