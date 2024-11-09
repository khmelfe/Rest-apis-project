#what to install
FROM python:3.12
#what port we will use
EXPOSE 5000
#what folder we will work on
WORKDIR /app
#what commands to run
RUN pip install flask
#where to copy all the files we need to what destinaion we want. two dots is to save at the same folder.
COPY  ./requirements.txt requirements.txt
#run to install requirements -we made this order ,so we won't install pip everytime we run(stored in cahe)
RUN pip install -r requirements.txt
#
COPY . .
#what command we should run what the image boots.
CMD [ "flask","run","--host","0.0.0.0" ]

#we did port fowarding to 5005.
#to run docker on cmd we use "docker run -p 5005:5000 <name of docker>"


##
#volume - to avoid rebuiling the code after every change we make volume
#volume will sync with host folder so that changes will be sync!
#making voulme by writing in the terminal 

# "docker run -dp 5000:5000 -w /app -v "/c/Documents/yourproject:/app" flask-smorest-api"
#-w /app - sets the container's present working directory where the command will run from.
#-v "$(pwd):/app" - bind mount (link) the host's present directory to the container's /app directory. 
#Note: Docker requires absolute paths for binding mounts, so in this example we use pwd for printing the absolute path of the working directory instead of typing it manually(IN Mac!).
#flask-smorest-api - the image to use.

#We using voulme so to run write : docker compose up 
#rebuilding the volume => docker compose up --build

