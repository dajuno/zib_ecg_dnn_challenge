====================
ZIB Coding Challenge
====================

by David Nolte


Introduction
============

We are going to use a deep neural network to classify ECG time series. Two communicating docker containers, for the database and the computation codes (via jupyter notebooks), need to be set up as indicated below.
Cf. the report :code:`doc/doc.pdf` for more details on the chosen components, data processing and the results.

Setup
=====

Create docker network
---------------------

Create a docker network in which the containers will be linked:

.. code:: shell

   docker network create challenge

Create database
---------------

Build and run docker environment:

.. code:: shell

   docker run --net challenge -p 27017:27017 --name mydb -d mongo:latest

Then execute the python script :code:`populate_db.py` to download the ECG dataset (https://zenodo.org/record/5711347/files/ECG_Rhythm_Lead_I.csv?download=1)
and data annotations (https://physionet.org/files/ptb-xl/1.0.1/ptbxl_database.csv?download)
and store them in the database:

.. code:: shell
   
   # outside the docker container, requirement: pymongo is installed (not mongodb)
   python3 docker_db/populate_db.py

For later sessions simply run

.. code:: shell

   docker start mydb

to activate the database.


Data analysis
-------------

Build and start JupyterLab container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Inside the folder :code:`docker_jl`, execute

.. code:: shell

   docker build -t jl_tf .

To create and start a persistent container, run:

.. code:: shell

   docker run --net challenge -p 8888:8888 -e JUPYTER_ENABLE_LAB=yes --name myjl jl_tf

To restart the container and notebook in a later session, run:

.. code:: shell

   docker start myjl
   docker exec myjl jupyter-lab


Run the test case of ECG signal classification 
==============================================

In JupyterLab, inside the folder :code:`work/`, execute the notebook :code:`ecg_resnet.ipynb` to:

1. connect to the data base, obtain and preprocess the timeseries data,
2. build the  ResNet (Residual Neural Network) model with keras as proposed by https://github.com/spdrnl/ecg/blob/master/ECG.ipynb,
3. train the ResNet with a portion of the data,
4. test the ResNet with data excluded from the training.

