FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN pip3 install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
