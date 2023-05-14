FROM python:3.10

EXPOSE 50051

WORKDIR /

COPY app app

COPY requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt
RUN ls -la

ENTRYPOINT ["python3", "-m" , "app"]
