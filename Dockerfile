FROM python:3.8.5
ADD . /code
WORKDIR /code
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python migrate.py
CMD python runserver.py
# CMD python app.py