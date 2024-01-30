from loader import load_and_merge_multi_ds
import glob 


paths = glob.glob('../cleaned_data/respirometry/*.nc')

ds = load_and_merge_multi_ds(paths)

