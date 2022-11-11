import pyedflib
import numpy as np
def extract_data(edf_path, time_len=20):
    f = pyedflib.EdfReader(edf_path) 
    n = f.signals_in_file
    print(f"number of datas:{n}")
    signal_labels = f.getSignalLabels()
    print(f"labels are:{signal_labels}")
    C3A2 = f.readSignal(3)
    C4A1 = f.readSignal(4)
    ECG = f.readSignal(5)
    SpO2 = f.readSignal(6)
    C3A2_frequency = f.getSampleFrequencies()[3]
    C4A1_frequency = f.getSampleFrequencies()[4]
    ECG_frequency = f.getSampleFrequencies()[5]
    SpO2_frequency = f.getSampleFrequencies()[6]


    print(f"C3A2 shape:{C3A2.shape} with sample frequency{C3A2_frequency}")
    print(f"C4A1 shape:{C4A1.shape} with sample frequency{C4A1_frequency}")
    print(f"ECG shape:{ECG.shape} with sample frequency{ECG_frequency}")
    print(f"SpO2 shape:{SpO2.shape} with sample frequency{SpO2_frequency}")
    print(f"whole duration:{f.getFileDuration()}")
    print(f"sample frequency in total:{f.getSampleFrequencies()}")



    ### read stage and respevt txt version file to get information of time and label
    with open('/content/vinsent_database/files/ucddb002_stage.txt') as in_stage:
        stage = in_stage.readlines()
    for i in range(len(stage)):
        stage[i] = int(stage[i].replace("\n",""))
    print(len(stage))
    with open('/content/vinsent_database/files/ucddb002_respevt.txt') as in_respevt:
        stage = in_respevt.readlines()
    stage_pure = stage[3:-1]
    print(len(stage_pure))



    ### extract info from raw data and restruct them 
    print(stage_pure[0])
    #[Time,Type,Duration,Low,%Drop,Rate,Change]
    [i for i in stage_pure[0].split(" ") if (i!="") and (i!="\n")]
    for i in range(len(stage_pure)):
        stage_pure[i] = [i for i in stage_pure[i].split(" ") if (i!="") and (i!="\n")]
    
    
    
    
    ### get start time of observation
    start_time = f.getStartdatetime()
    start_time_hour = start_time.hour





    ###extract start and duration of apnea happen relative to observation start time 
    from datetime import datetime,timedelta
    dict_of_apnea_time = dict()
    i = 0
    for i in range(len(stage_pure)):
        time_start = stage_pure[i][0]
        time_start_datetime_apnea = datetime.strptime(time_start,"%H:%M:%S")
        type = stage_pure[i][1]
        Duration = stage_pure[i][2]

        if time_start_datetime_apnea.hour<start_time_hour:
            start_time_hour = start_time_hour-24
        start_apnea_second = (time_start_datetime_apnea.hour-start_time_hour)*3600 + (time_start_datetime_apnea.minute-start_time.minute)*60 + (time_start_datetime_apnea.second-start_time.second)
        if type not in list(dict_of_apnea_time.keys()):
            dict_of_apnea_time[type] = [[start_apnea_second,Duration]]
        elif type in list(dict_of_apnea_time.keys()):
            dict_of_apnea_time[type].append([start_apnea_second,Duration])




    print(dict_of_apnea_time.keys())
    print(dict_of_apnea_time[list(dict_of_apnea_time.keys())[0]])




    ### make all apnea time and change thier staructure then sort them 
    all_apnea_time = []
    for item in list(dict_of_apnea_time.keys()):
        all_apnea_time.extend(dict_of_apnea_time[item])

    for i in range(len(all_apnea_time)):
        all_apnea_time[i] = [all_apnea_time[i][0],all_apnea_time[i][0] + int(all_apnea_time[i][1])]

    all_apnea_time = sorted(all_apnea_time, key=lambda x: x[0])





    ### extract non apnea time and add them to dict_of_apnea_time by key of 'Normal'
    starting_non_apnea = 0
    non_apnea_times = []
    for item in all_apnea_time:
        ending_non_apnea = item[0]
        non_apnea_times.append([starting_non_apnea,ending_non_apnea-starting_non_apnea])
        # non_apnea_times.append([starting_non_apnea,ending_non_apnea])
        starting_non_apnea = item[1]

    dict_of_apnea_time['Normal'] = non_apnea_times




    ###create continuose version and seprate version of apnea dictionary

    dict_of_apnea_data = dict()
    dict_of_apnea_data_continuous = dict()
    for type in list(dict_of_apnea_time.keys()):
        for i in range(len(dict_of_apnea_time[type])):
            start_time_one_item = dict_of_apnea_time[type][i][0]
            end_time_one_item = dict_of_apnea_time[type][i][0] + int(dict_of_apnea_time[type][i][1])
            C3A2_data = C3A2[start_time_one_item*C3A2_frequency:end_time_one_item*C3A2_frequency]
            C4A1_data = C4A1[start_time_one_item*C4A1_frequency:end_time_one_item*C4A1_frequency]
            ECG_data = ECG[start_time_one_item*ECG_frequency:end_time_one_item*ECG_frequency]
            SpO2_data = SpO2[start_time_one_item*SpO2_frequency:end_time_one_item*SpO2_frequency]
            if type not in list(dict_of_apnea_data.keys()):
                dict_of_apnea_data[type] = {
                    "C3A2_data":[C3A2_data],
                    "C4A1_data":[C4A1_data],
                    "ECG_data":[ECG_data],
                    "SpO2_data":[SpO2_data],
                }
                dict_of_apnea_data_continuous[type] = {
                    "C3A2_data":C3A2_data,
                    "C4A1_data":C4A1_data,
                    "ECG_data":ECG_data,
                    "SpO2_data":SpO2_data,
                }
            elif type in list(dict_of_apnea_data.keys()):
                dict_of_apnea_data[type]["C3A2_data"].append(C3A2_data)
                dict_of_apnea_data[type]["C4A1_data"].append(C4A1_data)  
                dict_of_apnea_data[type]["ECG_data"].append(ECG_data) 
                dict_of_apnea_data[type]["SpO2_data"].append(SpO2_data)


                dict_of_apnea_data_continuous[type]["C3A2_data"] = np.append(dict_of_apnea_data_continuous[type]["C3A2_data"],C3A2_data)
                dict_of_apnea_data_continuous[type]["C4A1_data"] = np.append(dict_of_apnea_data_continuous[type]["C4A1_data"],C4A1_data)  
                dict_of_apnea_data_continuous[type]["ECG_data"] = np.append(dict_of_apnea_data_continuous[type]["ECG_data"],ECG_data) 
                dict_of_apnea_data_continuous[type]["SpO2_data"] = np.append(dict_of_apnea_data_continuous[type]["SpO2_data"],SpO2_data)                           







    ###create generate_constant_time_dataset

    # time_len = 20 #len of time that you want to create your slice
    generate_constant_time_dataset = {}
    for type in list(dict_of_apnea_data_continuous.keys()):
        iteration = 0
        print(type)
        while True:
            if (time_len*C3A2_frequency*iteration+1)>len(dict_of_apnea_data_continuous[type]["C3A2_data"]):
                break
            if type not in list(generate_constant_time_dataset.keys()):
                # generate_constant_time_dataset[type]["C3A2_data"] = [dict_of_apnea_data_continuous[type]["C3A2_data"][iteration*time_len*C3A2_frequency:(iteration+1)*time_len*C3A2_frequency]]
                # generate_constant_time_dataset[type]["C4A1_data"] = [dict_of_apnea_data_continuous[type]["C4A1_data"][iteration*time_len*C4A1_frequency:(iteration+1)*time_len*C4A1_frequency]]
                # generate_constant_time_dataset[type]["ECG_data"] = [dict_of_apnea_data_continuous[type]["ECG_data"][iteration*time_len*ECG_frequency:(iteration+1)*time_len*ECG_frequency]]
                # generate_constant_time_dataset[type]["SpO2_data"] = [dict_of_apnea_data_continuous[type]["SpO2_data"][iteration*time_len*SpO2_frequency:(iteration+1)*time_len*SpO2_frequency]]
                generate_constant_time_dataset[type] = {
                    "C3A2_data" : [dict_of_apnea_data_continuous[type]["C3A2_data"][iteration*time_len*C3A2_frequency:(iteration+1)*time_len*C3A2_frequency]],
                    "C4A1_data" : [dict_of_apnea_data_continuous[type]["C4A1_data"][iteration*time_len*C4A1_frequency:(iteration+1)*time_len*C4A1_frequency]],
                    "ECG_data" : [dict_of_apnea_data_continuous[type]["ECG_data"][iteration*time_len*ECG_frequency:(iteration+1)*time_len*ECG_frequency]],
                    "SpO2_data" : [dict_of_apnea_data_continuous[type]["SpO2_data"][iteration*time_len*SpO2_frequency:(iteration+1)*time_len*SpO2_frequency]],
                }
            elif type in list(generate_constant_time_dataset.keys()):
                generate_constant_time_dataset[type]["C3A2_data"].append(dict_of_apnea_data_continuous[type]["C3A2_data"][iteration*time_len*C3A2_frequency:(iteration+1)*time_len*C3A2_frequency])
                generate_constant_time_dataset[type]["C4A1_data"].append(dict_of_apnea_data_continuous[type]["C4A1_data"][iteration*time_len*C4A1_frequency:(iteration+1)*time_len*C4A1_frequency])
                generate_constant_time_dataset[type]["ECG_data"].append(dict_of_apnea_data_continuous[type]["ECG_data"][iteration*time_len*ECG_frequency:(iteration+1)*time_len*ECG_frequency])
                generate_constant_time_dataset[type]["SpO2_data"].append(dict_of_apnea_data_continuous[type]["SpO2_data"][iteration*time_len*SpO2_frequency:(iteration+1)*time_len*SpO2_frequency])
            iteration = iteration + 1



    return generate_constant_time_dataset,dict_of_apnea_data

