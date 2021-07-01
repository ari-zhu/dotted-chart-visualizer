# Dotted Chart Visualizer

A a Python based, interactive Django app powered by [PM4PY](https://pm4py.fit.fraunhofer.de/), to display selected process data in the dotted chart visual style.

## Getting Started

### Starting the application

(The first two commands must be entered in the command prompt)

1. Installing necessary project dependencies:

   `python -m pip install -r requirements.txt`

2. In order to start the application, you can use:

   `python manage.py runserver`

3. To start using the dotted chart visualizer, type this in your browser:
   `http://127.0.0.1:8000/`

### Running the Unit Tests

To run the unit tests, run this command in the command prompt:
`python manage.py test`

### Running Dotted Chart Visualizer in a Docker container

1. Dockerfile is located in the project root folder (_UIFramework_pm4py_master_). Navigate to it.

2. Create a Docker Image by running this command in the command prompt: 
    `docker build --tag dcv .`

3. Start Dotted Chart Visualizer in a container using:
    `docker run --publish 8000:8000 dcv`

4. Access the dotted chart visualizer in your browser by entering:
    `http://127.0.0.1:8000/`
