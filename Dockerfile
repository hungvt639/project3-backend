FROM python:3.6.9
WORKDIR /app
ADD requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirments.txt
EXPOSE 8000
COPY . /app
CMD Main/manage.py makemigrations && Main/manage.py migrate && Main/manage.py runserver 0.0.0.0:8000