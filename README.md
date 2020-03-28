# Chainlink Python Serverless External Adapter Template

This template shows a basic usecase of an external adapter written in Python for the CryptoCompare API. It can be ran locally, in Docker, AWS Lambda, or GCP Functions.

## Install

```
pip3 install -r requirements.txt
```

## Test

```
python3 -m unittest tests/test_main.py
```

## Run with Docker

Build the image

```
docker build . -t cl-ea
```

Run the container

```
docker run -it -p 8080:8080 cl-ea
```

## Run with Serverless

### Create the zip

```bash
pip3 install --system --target ./package -r serverless_requirements.txt
cd package && zip -r ../cl-ea.zip . && cd ..
zip -g cl-ea.zip main.py
```

### Install to AWS Lambda

- In Lambda Functions, create function
- On the Create function page:
  - Give the function a name
  - Use Python 3.7 for the runtime
  - Choose an existing role or create a new one
  - Click Create Function
- Under Function code, select "Upload a .zip file" from the Code entry type drop-down
- Click Upload and select the `cl-ea.zip` file
- Change the Handler to `main.lambda_handler`
- Save


### Install to GCP

- In Functions, create a new function, choose to ZIP upload
- Use Python 3.7 for the runtime
- Click Browse and select the `cl-ea.zip` file
- Select a Storage Bucket to keep the zip in
- Function to execute: `gcs_handler`
