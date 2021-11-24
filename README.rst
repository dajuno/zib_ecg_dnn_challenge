====================
ZIB Coding Challenge
====================

Create database
===============

Build and run docker environment:

.. code:: shell

   docker build -t ecg_mongodb .
   docker run --name mydb ecg_mongodb

A MongoDB database containing a `ECG dataset<https://zenodo.org/record/5711347/files/ECG_Rhythm_Lead_I.csv?download=1>`_ will be created.
For later sessions, once the database is created, simply run

.. code:: shell

   docker start mydb

to activate the database.


Run the analysis
================

...
