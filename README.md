# Project Name : Log Analysis Automation (Python | Apache Airflow | PostgreSQL | CI/CD | Linux)

# Description Designed and implemented a fully automated log monitoring pipeline that scans application log files daily, detects and categorizes error patterns, and stores summarized reports in a PostgreSQL database for analysis.

# The workflow was orchestrated using Apache Airflow, ensuring scheduled and reliable execution, with backup cron jobs on Linux. Integrated a GitHub Actions CI/CD pipeline for automatic testing and deployment to an AWS EC2 environment, enabling seamless updates without manual intervention.

# airflow installation commands
AIRFLOW_VERSION=3.1.0

PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"

CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${A
IRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# steps to connect with the airflow UI for linux
step1 - create a project folder "airflow_project" and moving on to the project folder

step2 - install the virtualenv [sudo apt install python3-virtualenv] and create a virtualenv "airflow_venv"

step3 - start the venv with this command [source airflow_venv/bin/activate]

step4 - install the apache airflow latest version using the above mentioned commands "airflow installation commands"

step5 - set the airflow directory path for storing files related to airflow. command : [export AIRFLOW_HOME=~/airflow_project/airflow] 

step6 - from the project folder "airflow_project". run the command [airflow db migrate] for db and other files related to 
airflow setup inside "the ~/airflow_project/airflow"

step7 - start the api-server with the command : [airflow api-server --port 8080] 

step8 - after executed the step7. copy the user and password provided in the terminal.

step9 - Go to "http://localhost:8080" and put the user and password copied from the terminal.

step10 - Airflow UI connection with the working project folder is completed successfully. now you start the project.

# commands to see dag on the airflow ui
step1 - export AIRFLOW_HOME= ~/"mention-inbetween-directroy-names-if-presented"/airflow

step2 - airflow db migrate

step3 - airflow api-server 
        Note: run this on first terminal 

step4 - airflow scheduler
        Note: run this on second terminal

# "airflow api-server" and "airflow scheduler"

cmd: "airflow api-server" 

explanation: The Airflow API server provides the web-based UI and a REST API for users and services to interact with Airflow.

cmd: "airflow scheduler"

explanation: The Airflow scheduler is the persistent service that orchestrates and monitors all tasks and DAGs, triggering them to run when their dependencies are met. 

# if "airflow api-server" and "airflow scheduler" not working
then run this cmd

cmd: airflow standalone

