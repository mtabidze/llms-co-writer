## Prerequisites

- Python (3.11 or later)
- OpenAI API Key
- Redis server setup (locally or hosted) (optional)
- An AWS account and credentials (for DynamoDB) (optional)
- Docker (optional)

---

## Dependency Management

This project is built using poetry.

### Specifying Dependencies
To add a new package to your project, run the following command:
```shell
poetry add <package name>
```
To remove a package, use this command:
```shell
poetry remove <package name>
```
### Specifying Development Dependencies
For development-specific packages, use the following commands.
To add a development package:
```shell
poetry add <package name> --group dev
```
To remove a development package:
```shell
poetry remove <package name> --group dev 
```
### Lock File Update
To update the lock file, execute this command:
```shell
poetry lock
```
### Exporting Lock File to requirements.txt
To export the lock file to a requirements.txt file, use this command:
```shell
poetry export --without-hashes --format=requirements.txt > requirements.txt
```
### Installing Dependencies
To install project dependencies (excluding the root package), run:
```shell
poetry install --no-root 
```

---

## Docker Image Generation
To build a Docker image for this project, you can use the provided Dockerfile.
### Build Docker Image
To build the Docker image, run the following command in the project root directory:

```shell
docker build --tag <image name>:<image tag> .
```
### Run Docker Container
Once the image is built, you can run a Docker container using the following command:
```shell
docker run --publish 80:8080 --env <environment variables> <image name>:<image tag>
```

---

## Running the App
To run the application, we use the uvicorn ASGI server. Before running the application, make sure you set the all environment variables 
```shell
uvicorn app.main:create_app --reload
```
Once the server is running, you can access the application by navigating to http://127.0.0.1:8000 in your web browser.

---

## Testing
You can run various tests and code analysis tools using the provided scripts
### All Tests
To run all tests, execute:
```shell
./bin/run_all_tests.sh
```
### Unit Testing
For unit tests, use:
```shell
./bin/run_unit_testing.sh
```
### Functional Testing
To perform functional tests, run:
```shell
./bin/run_functional_testing.sh
```
### Coverage Measurement
Measure code coverage with:
```shell
./bin/run_coverage_measurement.sh
```
### Static Code Analysis
Conduct static code analysis with:
```shell
./bin/run_static_code_analysis.sh
```
