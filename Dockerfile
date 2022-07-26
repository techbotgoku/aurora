# init a base image (Alpine is small Linux distro)
FROM python:3.9.13-alpine
# update pip to minimize dependency errors 
RUN pip install --upgrade pip
# define the present working directory
WORKDIR /aurora-master
# copy the contents into the working dir
ADD . /aurora-master
# run pip to install the dependencies of the flask app
RUN pip install -r requirements.txt
# define the command to start the container
CMD ["python3","app.py"]