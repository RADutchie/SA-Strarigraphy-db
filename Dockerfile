FROM python:3.8.1-slim

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements
COPY ./requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# add prod entrypoint.sh
COPY ./entrypoint_prod.sh /usr/src/app/entrypoint_prod.sh

# add app
COPY . /usr/src/app

EXPOSE 8000
#EXPOSE 5432
RUN chmod +x entrypoint_prod.sh
# run server in prod
CMD ["./entrypoint_prod.sh"]
