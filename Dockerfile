# Use an official Python runtime as a parent image
FROM python:3.6-alpine
EXPOSE 8000
 
# Set the working directory to /app
WORKDIR /app
 
# Install python packages
RUN pip install Flask==1.0.2
RUN pip install PyGithub==1.40
RUN pip install PyYAML==3.13
RUN pip install gunicorn-19.9.0
 
# Copy the current directory contents into the container at /app
ADD . /app

CMD ["gunicorn", "-w 4", "-b 0.0.0.0", "app:app"]