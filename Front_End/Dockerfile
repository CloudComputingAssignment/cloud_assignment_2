#Docker file for IAM service
FROM python:3.9-slim
#working directory for docker
WORKDIR /APP  

#copy packages from requirement.txt
#COPY requirements.txt ./requirements.txt
COPY requirements.txt /APP/requirements.txt
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install -r requirements.txt

RUN git clone https://github.com/streamlit/streamlit-example.git .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]


