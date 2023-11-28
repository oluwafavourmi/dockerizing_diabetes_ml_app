# specify the base image
FROM continuumio/anaconda3:1.9.0

#create a new directory called . /usr/ML/app
COPY . /usr/ML/app

#expose port 5000 of docker to run this application
EXPOSE 5000

#change docker current working directoy to that of the local directory
WORKDIR /usr/ML/app

#install all the dependencies to help the app run
RUN pip install -r requirements.txt

#Docker to run the flask app
CMD python web.py