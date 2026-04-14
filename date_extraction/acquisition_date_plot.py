import matplotlib.pyplot as plt
import numpy as np
import os
from database.date_extraction.fct_date_extraction import LS_DataList
from database.date_extraction.fct_date_extraction import DateExtraction

def temporal_plot():
    try :
        path_1 = '/home/paudisio/Desktop/2023/S2_bis'
        path_2 = '/home/paudisio/Desktop/2023/L8_bis'

        S2_date = DateExtraction.EEG_date_extraction(path_1)
        L8_date = DateExtraction.HLS_date_extraction(path_2)

        S2_date = np.array(S2_date, dtype='datetime64').astype('O')
        L8_date = np.array(L8_date, dtype='datetime64').astype('O')


        # Plotting histogram of the different date

        #Y_year, M_months, W_week, D_day
        x = np.arange('2023-01-01', '2024-01-15', dtype='datetime64[W]').astype('O')

        plt.figure()
        plt.title('Acquisitions S2 et L8 année 2023')
        plt.hist(S2_date, bins=x, histtype='barstacked', alpha = 0.5,  rwidth=0.5, label='S2_date')
        plt.hist(L8_date, bins=x, histtype='barstacked', alpha = 0.5, rwidth=0.5, label='L8_date')
        plt.xticks(x[::2])
        plt.tick_params(axis='x', labelsize=7, labelrotation=35)
        plt.legend(loc="upper right")
        plt.show()

    except IOError as e:
        print("An error occurred:", e)
