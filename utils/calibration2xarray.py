from csv2xarray import csv2xarray
import glob

calibration_files = glob.glob('raw_data/calibration/*.csv')

for file in calibration_files:
    print(file)
    csv2xarray(file, is_calibration=True)