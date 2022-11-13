# apnea_data_augmentation_by_concatenation
one of the problem in apnea classification and using databases is length of time that apnea happen and it should be more than special time(usually 20 second) so we lost a lot of data that are less than that of so in this code i try to get all time of from each type of apnea and concatenate them together and slicing them in that special time

the idea implement on vincent's database 

in this code I extract this data that commonly important than other data:
C3A2_data
C4A1_data
ECG_data
SpO2_data

<h3>make database for all user</h3><br/>
by using extract_struct_data.py try to create pkl database for each user with below path:
case_name -> type_of_apnea or normal -> type_of_data(C3A2_data,C4A1_data,ECG_data,SpO2_data) -> list_of_data
and save them in 2 type of database:
whole_database_apnea_constant.pkl:
that include consistant time cut of concatenated data of apnea and normal data
whole_database_apnea.pkl:
include raw data in structured way
this code implement in "apnea_create_all_database.ipynb"

<h3>classification with lstm </h3><br/>
in this part we try to create and preprocessing data for giving it to lstm RNN and then generate RNN model and train it the codes are implement in "apnea_RNN.ipynb"
and we create 3 type of model one for C3A2 only ,one for C4A1 and one for concatenate of them 
