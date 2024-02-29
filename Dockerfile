FROM continuumio/miniconda3

WORKDIR /app

COPY ./environment.yml .

RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "project-altituderando", "/bin/bash", "-c"]
#SHELL ["/bin/bash", "-c"]


COPY src/. ./src
COPY data/. ./data

#ENTRYPOINT ["sleep", "1000"]
#CMD ls -la
#ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "myenv", "python", "./src/insertion.py"]
#CMD conda run ./src/insertion.py
#CMD ["bash"]
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "project-altituderando"]
CMD ["python" , "./src/insertion.py"]