# Built with help from
# https://softwarejargon.com/dockerizing-python-flask-app-and-conda-environment/

FROM continuumio/miniconda:latest

WORKDIR /app

#COPY environment.yml ./
#COPY app/ ./
#COPY data/ ./
#COPY boot.sh ./
COPY . /app

RUN chmod +x boot.sh

RUN conda env create -f environment.yml

RUN echo "conda activate proj" >> ~/.bashrc
ENV PATH /opt/conda/envs/proj/bin:$PATH

EXPOSE 5000

ENTRYPOINT ["sh", "./boot.sh"]
