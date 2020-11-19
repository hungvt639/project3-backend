<<<<<<< HEAD
FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PORT 8000

=======
FROM python:3.6.9
RUN mkdir /app
>>>>>>> 76eb2b94912d4da124b4ef4a1598ab13034c373f
WORKDIR /app

COPY requirments.txt /app/requirments.txt
RUN pip install --upgrade pip && pip install -r requirments.txt
COPY . /app
<<<<<<< HEAD
EXPOSE 8000

CMD Main/manage.py makemigrations && Main/manage.py migrate && Main/manage.py runserver 0.0.0.0:8000


RUN chmod +x start.sh

CMD ["./start.sh"]
=======
CMD Main/manage.py makemigrations && Main/manage.py migrate && Main/manage.py runserver 0.0.0.0:8000
>>>>>>> 76eb2b94912d4da124b4ef4a1598ab13034c373f
