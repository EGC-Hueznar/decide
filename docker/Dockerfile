from python:3.7-alpine

RUN apk add --no-cache git postgresql-dev gcc libc-dev
RUN apk add --no-cache gcc g++ make libffi-dev python3-dev build-base
RUN apk add --update nodejs=12.20.1-r0
RUN apk add --update npm
RUN pip install gunicorn
RUN pip install psycopg2
RUN pip install ipdb
RUN pip install ipython

WORKDIR /app

RUN git clone -b releaseM3 https://github.com/EGC-Hueznar/decide  .
RUN pip install -r requirements.txt

WORKDIR /app/decide/booth/decide-react
RUN npm install
RUN npm install --global expo-cli
RUN expo build:web

WORKDIR /app/decide
# local settings.py
ADD docker-settings.py /app/decide/local_settings.py
RUN ./manage.py collectstatic

RUN cp -r booth/decide-react/web-build/static/js ../static

CMD ["gunicorn", "-w 5", "decide.wsgi", "--timeout=500", "-b 0.0.0.0:5000"]
