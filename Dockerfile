FROM python:3

EXPOSE 80

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY *.py /app/

ENTRYPOINT [ "python", "/app/main.py" ]
CMD ["--listen", "80"]