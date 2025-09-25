FROM python

WORKDIR /proyecto

COPY src/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /proyecto

CMD ["python", "src/main.py"]