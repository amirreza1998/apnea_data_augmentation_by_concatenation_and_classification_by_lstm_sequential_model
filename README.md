# apnea_data_augmentation_by_concatenation
one of the problem in apnea classification and using databases is length of time that apnea happen and it should be more than special time(usually 20 second) so we lost a lot of data that are less than that of so in this code i try to get all time of from each type of apnea and concatenate them together and slicing them in that special time

the idea implement on vincent's database 

in this code I extract this data that commonly important than other data:
C3A2_data
C4A1_data
ECG_data
SpO2_data

#classification with lstm 
load database and create pkl database for each user with below path:
case_name -> type_of_apnea or normal -> type_of_data(C3A2_data,C4A1_data,ECG_data,SpO2_data) -> list_of_data
#classification with lstm 
