FROM python:3

WORKDIR /usr/src/app

EXPOSE 4444

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "./app.py" ] 
