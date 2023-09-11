FROM python:3.9

WORKDIR /usr/src/app

EXPOSE 4444

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src src
COPY app.py .

ENTRYPOINT [ "python", "./app.py" ] 
