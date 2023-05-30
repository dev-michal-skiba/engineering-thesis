# Run app
## Requirements
Below docker versions were used while developing project
- docker: 24.0.2
- docker-compose: 1.29.2
## Build docker image
```commandline
./bin/build_image
```
## Run app in docker container
App should be running on http://localhost:8000
```commandline
./bin/run_app
```

# Testing the app
File `postman_collection.json` contains ready to use Postman collection that provides request to 
test all API endpoints of the application
