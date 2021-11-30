FROM jupyter/tensorflow-notebook

USER root
# install iputils for ping command ... to test networking
RUN apt-get update && apt-get install -y iputils-ping

USER jovyan
RUN pip install pymongo tensorflow_addons jupyterlab-vim

COPY ecg_resnet.ipynb database.ipynb helper_functions.ipynb plot_timeseries.ipynb /home/jovyan/work/
