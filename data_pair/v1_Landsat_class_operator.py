import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import csv
import rasterio
import torch


class raster_data():
    @staticmethod
    def array2raster(raster, array, outpath):
        kwargs = raster.meta
        kwargs.update(dtype=rasterio.float32, count=1)

        with rasterio.open(outpath, 'w', **kwargs) as dst:
            dst.write_band(1, array.astype(rasterio.float32))
    @staticmethod
    def import_raster_data(path2raster):
        raster = rasterio.open(path2raster)
        array = raster.read(1)

        return (array)


class little_pair(raster_data):
    @staticmethod
    def crop_pair(number_pairs, size, path2tensor, path2raster_centerline):
        try:
            spectral_tensor = torch.load(path2tensor,weights_only=True)
            spectral_tensor = spectral_tensor.permute(2,0,1).unsqueeze(0)
            array_centerline = little_pair.import_raster_data(path2raster_centerline)
        except Exception as e:
            print(e)
            return()

        d, n, r, c = spectral_tensor.size()


        half_size = size // 2
        batch_max = c // size
        shift_tmp = half_size
        square_crop_dict = {}

        nb_data = 0

        print(f"Max number of batch of size {size} is {batch_max}")

        while nb_data < (number_pairs-1):
            nb_data = nb_data + 1

            r_array = np.where(array_centerline[:, shift_tmp] == 1)[0]
            r_array_tmp = r_array[0]

            r_tensor_1 = r_array_tmp - half_size
            r_tensor_2 = r_array_tmp + half_size
            c_tensor_1 = shift_tmp - half_size
            c_tensor_2 = shift_tmp + half_size

            if r_tensor_1 < 0 or r_tensor_2 > r or c_tensor_1 < 0 or c_tensor_2 > c:
                print(0,r,0,c)
                print(r_tensor_1, r_tensor_2, c_tensor_1, c_tensor_2)
                return()

            else:
                square_crop = torch.zeros(size, size)
                square_crop[:,:] = spectral_tensor[0, 0, r_tensor_1:r_tensor_2, c_tensor_1:c_tensor_2]

                square_crop_dict[str(nb_data)] = square_crop

                plt.figure(), plt.imshow(square_crop), plt.show()

                shift_tmp = shift_tmp + half_size

        return (square_crop_dict)