FROM python:3.11-slim

COPY Modeling/Regressions:Classifications/causal.py /pyeng/

COPY requirements.txt /pyeng/

WORKDIR /pyeng

COPY data/titanic.csv /pyeng/data/

RUN pip install -r requirements.txt

CMD ["python", "causal.py"]
