import csv
from pymongo import MongoClient

CSV_FILE = "ECG_Rhythm_Lead_I.csv"


def read_csv(csv_file):
    """Convert CSV file to JSON.

    Args:
        csv_file (str): path of csv data file

    Returns:
        list:   list of data set dicts (per csv row)
    """
    datasets = []

    print("reading CSV data")

    with open(csv_file, "r") as fp:
        reader = csv.DictReader(fp)

        i_start = 7
        meta = reader.fieldnames[1:i_start]
        times = reader.fieldnames[i_start:]

        for row in reader:
            data_dict = {m: row[m] for m in meta}
            data_dict["data"] = [
                float(row[str(i)]) for i in range(i_start, len(times))
            ]
            datasets.append(data_dict)

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

    print("creating collection from datastes")
    collection.insert_many(datasets)

    # for d in collection.find({"ecg_id": "1"}):
    #     print(d)


if __name__ == "__main__":
    datasets = read_csv(CSV_FILE)
    create_db(datasets)
