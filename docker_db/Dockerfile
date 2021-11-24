FROM mongo:latest

# install python, wget and download CSV file
RUN set -ex; \
    apt-get update; \
    apt-get install -y wget python3 python3-pymongo vim-tiny; \
    wget --read-timeout=10 -nc -nv -O /ECG_Rhythm_Lead_I.csv \
    "https://zenodo.org/record/5711347/files/ECG_Rhythm_Lead_I.csv?download=1";

COPY create_db.py /
# COPY ECG_Rhythm_Lead_I.csv /
