FROM python:3.11.2

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc vim

RUN useradd -rms /bin/bash django && chmod 777 /opt /run

WORKDIR /project

RUN mkdir /project/static && chown -R django:django /project && chmod 755 /project

COPY --chown=django:django /app .

RUN pip install -r requirements.txt

USER django

CMD ["gunicorn","-b","0.0.0.0:8000","config.wsgi:application"]
