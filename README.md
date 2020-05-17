# Contract tests for User Service

This git repository contains contract tests for [User Service](https://github.com/LukasForst/SWA-TP-user-service).
It uses clean docker image pulled from the Docker hub.
 
## Running
Ensure that you have python and pip installed, then run `pip install -r requirements.txt` to install dependencies.
 
To execute contract tests run `make test`.
It cleans cache (if there's any) and downloads latest docker image of service and starts it up.
Then the tests are executed locally. 