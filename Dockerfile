FROM continuumio/miniconda3
ADD Softlab.yml /tmp/Softlab.yml
RUN conda config --set ssl_verify no
RUN conda env create -f /tmp/Softlab.yml
RUN echo "source activate $(head -1 /tmp/Softlab.yml | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 /tmp/Softlab.yml | cut -d' ' -f2)/bin:$PATH
# Create app directory
WORKDIR /usr/src/app
COPY . .

EXPOSE 8000
CMD [ "python3", "main.py" ]