### Application overview
The **LinkShortner** is a django application running in a docker container which communicate to frontend through django rest API. 

*Gunicorn* is used as app server for running the wsgi application. *Nginx* is used for proxy server which runs inside the docker container and communicate through port 8000.

The frontend interface can be accessed at localhost:8000 where we can generate short link for any url.

### Running the application
##### Requirements
- For running the application in docker container, **Docker** needs to be installed in the system if not already installed. Please follow the instruction for the installation: https://docs.docker.com/get-docker/

- Clone the project repo: git clone https://github.com/sandip-ghimire/LinkShortner

##### Steps
- Open the command line from the root directory of the project, i.e. the path where dockerfile is located.  Build the docker image with the command:
  >docker build -t short-link .
  
- Run the docker container with the command below: <br />
  The length of the resulting short link and the url can be configured through env. variables while running the container. The env. variables can be altered at .env file present in project root. <br />
  - HEX_CODE_LENGTH: It defines how long the code should be in the short url. Default is 8. <br />
  - PRE_URL: The url used for short link can be configured with this variable. Default is 'http://bit.ly' <br />
  *While running the container '--env-file .env' part is optional. If env variables are not provided the application takes default values.*
  <br />
  
  >docker run --name=short_link --env-file .env -p 8000:8000 short-link
  
  *(The application runs on port 8000)* <br />
  The interface can be accessed at: <br />
  http://localhost:8000/
  
### Testing the application
###### Unit Test
- While the application is running, it can be tested primarily using unit test. Command for unit test:
    >docker exec -it short_link ./manage.py test
  - The output should be 'OK' if the test is successful.
    
