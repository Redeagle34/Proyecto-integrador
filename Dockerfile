FROM python:3.13.1

WORKDIR /proyecto

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /proyecto

CMD ["python", "main.py"]