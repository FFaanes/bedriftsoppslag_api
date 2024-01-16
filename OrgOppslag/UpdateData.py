import os
import shutil

import pandas as pd
import numpy as np
import gzip
import urllib.request

base_path = os.path.realpath(os.path.dirname(__file__))



def download_new_brreg():
    print("1/4: Downloading CSV containing all companies.")
    with urllib.request.urlopen("https://data.brreg.no/enhetsregisteret/api/enheter/lastned/csv") as response:
        with gzip.GzipFile(fileobj=response) as uncompressed:
            file_content = uncompressed.read()
    with open(os.path.join(base_path, f"./data/temp/all.csv"), 'wb') as f:
        f.write(file_content)
        print("1/4: DONE.")


def separate_csv_by_firstletter():
    print("2/4: Separating companies into files by first letter.")
    all = pd.read_csv(os.path.join(base_path,"./data/temp/all.csv"), low_memory = False).replace(np.NaN, None)
    all["navn"] = all["navn"].str.upper()
    grouped = all.groupby(all.navn.str[0])
    for group in grouped:
        pd.DataFrame(group[1], columns=["organisasjonsnummer","navn"]).to_csv(os.path.join(base_path, f"./data/temp/{ord(group[0].lower())}.csv"), index=False)
    print("2/4: DONE.")


def delete_old_brreg_csv():
    print("3/4: Deleting old csv files.")
    old_csv_files = os.listdir(os.path.join(base_path,"./data"))
    for file in old_csv_files:
        if file == "temp":
            continue
        os.remove(os.path.join(base_path,f"./data/{file}"))
    print("3/4: DONE.")


def move_temp_to_data():
    print("4/4: Moving files from temp into data")
    temp_folder_files = os.listdir(os.path.join(base_path,"data","temp"))
    for file in temp_folder_files:
        shutil.move(os.path.join(base_path,"data","temp",file), os.path.join(base_path,"data",file))
    os.remove(os.path.join(base_path,"data","all.csv"))
    print("4/4: DONE")


# Main Function
def update_brreg_files():
    download_new_brreg() # Download csv with all companies into temp
    separate_csv_by_firstletter() # Separate companies into csv by first letter
    delete_old_brreg_csv() # Delete old csv files
    move_temp_to_data() # Transfer all files from temp into data
    print("DONE: Updated Company Data.")



# Update data
if __name__ == "__main__":
    update_brreg_files()