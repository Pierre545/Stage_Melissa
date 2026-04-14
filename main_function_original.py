import numpy as np
import pandas as pd
import rasterio
import torch
import os
from date_extraction.fct_date_extraction import LS_DataList
from date_extraction.fct_date_extraction import DateExtraction
from collections import Counter
import shutil

class main_fct():

    @staticmethod
    def SL_create_csv(path_1, path_2):
    # Create two csv file containing path to data, and associate a class to each element depending on the temporal acquisition

        try :
            # Y_year, M_months, W_week, D_day
            # Création d'une liste de date éspacé d'une semaine
            x       = np.arange('2023-01-01', '2024-01-15', dtype='datetime64[W]').astype('O')


            #Extract acquisition date and changing format
            S2_date = DateExtraction.EEG_date_extraction(path_1)
            L8_date = DateExtraction.HLS_date_extraction(path_2)

            S2_date = np.array(S2_date, dtype='datetime64').astype('O')
            L8_date = np.array(L8_date, dtype='datetime64').astype('O')


            # Data histrograms
            S2_count,S2_bin = np.histogram(S2_date,x)
            L8_count,L8_bin = np.histogram(L8_date,x)

            # List of path file sorted
            S2_files        = LS_DataList.extract_path(path_1)
            L8_files        = LS_DataList.extract_path(path_2)

            S2_files        = np.sort(S2_files)
            L8_files        = np.sort(L8_files)


            # Associate to each element of "count_list" a letter corresponding to a specific bin
            S2_count         = LS_DataList.new_class_list(S2_count)
            L8_count         = LS_DataList.new_class_list(L8_count)

            # Adjust size of the data list depending on the Null values in count list
            S2_files         = LS_DataList.adjust_list(S2_count, S2_files)
            L8_files         = LS_DataList.adjust_list(L8_count, L8_files)


            # Create a pd DataFrame
            S_dataframe    = pd.DataFrame({'class': S2_count,

                                           'path': path_1,

                                           'data': S2_files})

            L_dataframe    = pd.DataFrame({'class': L8_count,

                                            'path': path_2,

                                            'data': L8_files})

            S2_counter     = Counter(S2_count)
            L8_counter     = Counter(L8_count)

            pairs = 0
            for data in L_dataframe['class']:
                pairs = pairs + (L8_counter[str(data)] * S2_counter[str(data)])
            print("Number of full images pairs available :", pairs)

            outpath_1 = "./data_pair/L_out.csv"
            outpath_2 = "./data_pair/S_out.csv"

            L_dataframe.to_csv(outpath_1, index=False)
            S_dataframe.to_csv(outpath_2, index=False)

            # print("Outpath folder of extracted date : /home/paudisio/PycharmProjects/Super_resolution/pythonProject/database/date_extraction/Data_class_csv/")

            return(str(outpath_1), str(outpath_2))

        except IOError as e:
            print("An error occurred:", e)


    @staticmethod
    def tensor_creator(path_1,path_2,number_files=None):
        """
        : Sentinel2 tensor contains the following bands ["B2", "B3", "B4", "B8"], Landsat tensor contains the following bands ["B02", "B03", "B04", "B05"]
        : if number_files is None then it takes the maximum value
        :param path_1 variable should be the path to the csv file containing all the paths of the different pair, for example the one created with write_dict function
        :param path_2 should be the path of the folder wich will contain all the output
        """

        output_path = str(path_2)
        if os.path.exists(output_path):
            shutil.rmtree(output_path)
        os.makedirs(output_path, exist_ok=True)

        df = pd.read_csv(path_1)

        data_size  = len(df["data_1"])

        if number_files is None:
            number_files = data_size
            print("Number of files available :", number_files)
        else:
            number_files = number_files


        ##############################
        #Here the value 3 should be changed with number_files if we want the pair fo all the elements
        ##############################
        for i in range (number_files):
            print(f"File number {i} of {number_files}")

            dict_1 = {}
            dict_2 = {}
            path_1 = df["data_1"][i]
            try:
                file_1 = os.listdir(path_1)

                # Third dimension counter for created tensor
                n = 0
                for j in file_1:
                    # For Landsat
                    if any(x in j for x in ["B02","B03","B04","B05"]) and "xml" not in j:
                        #Open raster
                        print(f"file name: {j}")
                        path_raster_1 = os.path.join(path_1,j)
                        raster_1 = rasterio.open(path_raster_1)

                        #Create a tensor of size N*N*4
                        array_1 = raster_1.read(1)

                        if (n==0):
                            c,r     = np.shape(array_1)
                            torch_tensor = torch.empty((c,r,4))

                        torch_tensor[:,:,n] = torch.from_numpy(array_1)
                        n=n+1
                #Permute allows to set the channel as the first dimension
                dict_1[f"torch_tensor_{j[:-4]}"] = torch_tensor.permute(2,0,1).unsqueeze(0)

            except :
                print("Error_1")
                pass



            path_2 = df["data_2"][i].split("'")[1::2]
            try:
                nb_path = len(path_2)
                for z in range (nb_path):
                    tmp_path = path_2[z]
                    #file_2 = os.listdir(os.path.join(path_1, tmp_path))
                    file_2 = os.listdir(tmp_path)

                    # Third dimension counter for created tensor
                    n = 0
                    for j in file_2:
                        #For Sentinel-2
                        if any(x in j for x in ["B2", "B3", "B4", "B8"]) and "xml" not in j:
                            print(f"file name: {j}")
                            # Open raster
                            path_raster_2 = os.path.join(tmp_path, j)

                            raster_2 = rasterio.open(path_raster_2)

                            # Create a tensor of size N*N*4
                            array_2 = raster_2.read(1)

                            if (n==0) :
                                c, r = np.shape(array_2)
                                torch_tensor = torch.empty((c, r, 4))

                            torch_tensor[:, :, n] = torch.from_numpy(array_2)
                            n = n + 1

                    dict_2[f"torch_tensor_{j[:-7]}"] = torch_tensor.permute(2,0,1).unsqueeze(0)

            except:
                print("Error_2")
                pass

            new_path = os.path.join(output_path,f"HR_LR_{i}")
            os.makedirs(new_path)
            for i in (dict_1.keys()):
                torch.save(dict_1[str(i)], os.path.join(new_path, i))
            for j in (dict_2.keys()):
                torch.save(dict_2[str(j)], os.path.join(new_path, j))

        # return(dict_1, dict_2)


