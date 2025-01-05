# FastAPI Project

This is a FastAPI project that can be run using `uvicorn`. Below are the steps to set up the environment, install dependencies, and start the project.

## Prerequisites

- Python 3.11
- `virtualenv` (for creating virtual environments)

## Setup Instructions

### Step 1: Clone the Repository

Clone this repository to your local machine or AWS EC2 instance:

```bash
git clone https://github.com/swarupOGM/math_skill.git
cd math_skill
```

## Install virtualenv
```
pip install virtualenv
```
## Activate the Virtual Environment
```
virtualenv -p python3 venv (to create)
source venv/bin/activate (to activate)
```
## Install Project Dependencies

```
pip install -r requirements.txt
```
## Run the Project with uvicorn
```
uvicorn main:app --reload --port 8080
```
## You can now access the app at
```
http://localhost:8080
```

## Here is the cURL
```
curl --location 'http://localhost:8080/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "john.doe@example.com",
    "password": "password123"
}'
```
For register:
```
curl --location 'http://localhost:8080/register' \
--header 'Content-Type: application/json' \
--data-raw '{
    "first_name": "Swarup",
    "last_name": "Adhikary",
    "email": "swarupovo@gmail.com",
    "age": 25,
    "user_class": "Class A",
    "country": "USA",
    "password": "password123",
    "confirm_password": "password123"
}'
```
