FROM python:3.9

EXPOSE 4444

WORKDIR /usr/src/app
COPY . /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app/test
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "-m", "pytest", "-v" ] 
