FROM python:3.10
ARG DIR=/code

WORKDIR $DIR

RUN apt-get update && apt-get upgrade -y

COPY requirements.txt ./

RUN python3 -m pip install --upgrade pip

RUN apt-get install nano -y

RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .

# uWSGI will listen on this port
EXPOSE 8050

# Install uWSGI
RUN pip install uwsgi

# Start uWSGI
CMD ["uwsgi", "--ini", "uwsgi.ini"]