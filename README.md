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

### Running app without CSRF protection
```commandline
./bin/run_app_without_csrf_protection
```

### Running app with Double Submit Cookie CSRF protection
```commandline
./bin/run_app_with_dsc_csrf_protection
```

# Testing the app

## Manual tests
File `postman_collection.json` contains ready to use Postman collection that provides request to 
test all API endpoints of the application

## Load tests
Tests are performed for one minute, with 2 users spawning each second with maximum of 10 users
at one moment calling the API

### Load testing app without CSRF protection
The result of such test is located in `app/tests/test_load/results/protection_off.html` file.

To recreate the test on your machine follow this steps

1. In one terminal run below command to start app without CSRF protection
```commandline
./bin/run_app_without_csrf_protection
```
2. Wait for app to be fully set up
3. In the other terminal run below command to clear database from users
```commandline
docker exec -it engineering_thesis_db psql -U postgres -c "DELETE FROM users;"
```
3. Run below command to run the load test
```commandline
cd ./app && locust --config tests/test_load/test_protection_off/locust.conf
```
4. Wait for 60 seconds for the test to finish
5. New results should be in `app/tests/test_load/results/protection_off.html` file.

### Load testing app with Double Submit Cookie CSRF protection
The result of such test is located in `app/tests/test_load/results/double_submit_cookie.html` file.

To recreate the test on your machine follow this steps

1. In one terminal run below command to start app with Double Submit Cookie CSRF protection
```commandline
./bin/run_app_with_dsc_csrf_protection
```
2. Wait for app to be fully set up
3. In the other terminal run below command to clear database from users
```commandline
docker exec -it engineering_thesis_db psql -U postgres -c "DELETE FROM users;"
```
3. Run below command to run the load test
```commandline
cd ./app && locust --config tests/test_load/test_double_submit_cookie/locust.conf
```
4. Wait for 60 seconds for the test to finish
5. New results should be in `app/tests/test_load/results/double_submit_cookie.html` file.
