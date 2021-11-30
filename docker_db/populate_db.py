#!/usr/bin/env python3
import csv
import hashlib
import urllib.request
from pathlib import Path

from pymongo import MongoClient

CSV_FILE1 = "ECG_Rhythm_Lead_I.csv"
URL_DATA1 = (
    "https://zenodo.org/record/5711347/files/ECG_Rhythm_Lead_I.csv?download=1"
)
MD5_SUM1 = "9752903f3eeff7791383fa5fce9f0e5a"

CSV_FILE2 = "ptbxl_database.csv"
URL_DATA2 = (
    "https://physionet.org/files/ptb-xl/1.0.1/ptbxl_database.csv?download"
)
MD5_SUM2 = "2c5ad83072e99e3ef017624759c4735b"


def md5(fname):
    """Get MD5 of file. taken from: https://stackoverflow.com/a/3431838"""
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def download_data(url, dlfile, md5sum, force=False):
    """Download CSV file, if file does not exist.

    Args:
        url (str): url to file
        dlfile (str): name of file to be saved
        force (bool): if True, overwrite existing file
    """
    if Path(dlfile).exists():
        print(f"{dlfile} exists, skipping download.")
    else:
        print(f"Downloading data from {url} to {dlfile}.")
        urllib.request.urlretrieve(url, dlfile)

    # check file integrity
    if md5(dlfile) == md5sum:
        print("checking file integrity... md5 checksum correct")
    else:
        raise Exception(
            f"{dlfile}: wrong md5 checksum. delete file and " "retry"
        )


def read_csv(csv_file, ftype=1):
    """Read csv data and store in list of dicts.

    Args:
        csv_file (str): path of csv data file
        ftype (int): file type: 1 = data csv, 2 = meta data csv

    Returns:
        list:   list of data set dicts (per csv row)
    """
    datasets = []

    print("reading CSV data")

    with open(csv_file, "r") as fp:
        reader = csv.DictReader(fp)

        if ftype == 1:
            i_start = 7
            meta = reader.fieldnames[1:i_start]
            times = reader.fieldnames[i_start:]

            for row in reader:
                data_dict = {m: row[m] for m in meta}
                data_dict["data"] = [float(row[t]) for t in times]
                datasets.append(data_dict)

        else:
            for row in reader:
                datasets.append(
                    {"ecg_id": row["ecg_id"], "strat_fold": row["strat_fold"]}
                )

    print(f"read CSV data with {len(datasets)} rows")

    return datasets


def create_db(datasets):
    """Create MongoDB database.

    Args:
        datasets (list): list of data dicts
    """
    print("connecting with MongoDB...")
    client = MongoClient(port=27017)
    db = client.zib
    # delete existing collection
    db.drop_collection("ecg_data")
    collection = db.ecg_data

    print("creating collection from datasets")
    collection.insert_many(datasets)

    # for d in collection.find({"ecg_id": "1"}):
    #     print(d)


def merge_data_stratfold(data, descriptors):
    """Merge data and strat_fold from data file and descriptors file."""
    # a little clumsy but does the job ...
    ecg_ids = []
    ecg_ids2 = []
    # data_dict = {}
    for d in data:
        eid = int(d["ecg_id"])
        ecg_ids.append(eid)
        # data_dict[eid] = d

    desc_dict = {}
    for d in descriptors:
        eid = int(d["ecg_id"])
        ecg_ids2.append(eid)
        desc_dict[eid] = d

        if eid in ecg_ids:
            idx = ecg_ids.index(eid)
            data[idx]["strat_fold"] = int(d["strat_fold"])
        else:
            print(f"ecg_id {eid} not found in data!")

    diff = set(ecg_ids).difference(ecg_ids2)
    print(f"Size ECG datasets: {len(ecg_ids)}")
    print(f"Size meta data: {len(ecg_ids2)}")
    print(f"Number of ID non-matches: {len(diff)}")

    return data


if __name__ == "__main__":
    download_data(URL_DATA1, CSV_FILE1, MD5_SUM1)
    download_data(URL_DATA2, CSV_FILE2, MD5_SUM2)
    datasets = read_csv(CSV_FILE1, 1)
    data_descriptors = read_csv(CSV_FILE2, 2)
    data_merged = merge_data_stratfold(datasets, data_descriptors)
    create_db(data_merged)
