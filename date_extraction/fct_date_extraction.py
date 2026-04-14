import numpy as np
import os
from datetime import datetime
from string import ascii_lowercase
import itertools
import matplotlib.pyplot as plt
import os

class DateExtraction():
    def EEG_date_extraction(self):
        folders = os.listdir(self)
        date = []

        for i in folders:
            tmp_date = i[:-30]
            date_obj = datetime.strptime(tmp_date, "%Y%m%d")
            gregorian_date = date_obj.strftime("%Y-%m-%d")

            date.append(gregorian_date)

        return (date)

    def HLS_date_extraction(self):
        folders = os.listdir(self)
        date = []

        for i in folders:
            tmp_date = i[15:-12]
            #strptime convert a string that represents a date/time into a datetime object
            julian_date = datetime.strptime(str(tmp_date), '%Y%j')
            #strftime convert a datetime object into a formatted string
            gregorian_date = datetime.strftime(julian_date, '%Y-%m-%d')

            date.append(gregorian_date)

        return (date)


class LS_DataList():
    def extract_path(self):
        folders = os.listdir(self)

        path_files = []
        for i in folders:
            path_files.append(i)

        return (path_files)


    # Create a list of characters
    def iter_all_strings():
        for size in itertools.count(1):
            for s in itertools.product(ascii_lowercase, repeat=size):
                list = yield "".join(s)


    #Associate to the number in the count list of histogram a letter
    def new_class_list(self):
        d          = 0
        n          = sum(self)
        alpha_tmp  = itertools.islice(LS_DataList.iter_all_strings(), 0, n, 1)
        alpha_list = []
        for i in alpha_tmp:
            alpha_list.append(i)

        new_list   = []
        for i in self:
            if i == 0:
                new_list.append(0)
            else:
                for j in range(i):
                    new_list.append(alpha_list[d])
                d = d + 1
        return (new_list)


    # list_1 should be the one containing 0, a list of the same size of the first completing the second with zero
    def adjust_list(self, list_1):
        len_0 = len(self)

        #print("ERROR: list_0 should contain 0 value")

        for i in range(len_0):
            if self[i] == 0:

                #Transform an array into a list instead of the following
                list_1 = np.array([list_1])
                list_1 = np.append(list_1,0)

                list_1[i+1:] = list_1[i:-1]
                list_1[i] = 0

        return (list_1)