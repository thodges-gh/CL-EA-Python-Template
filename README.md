# Chainlink Python Serverless External Adapter Template

![Lint and unit testing](https://github.com/thodges-gh/CL-EA-Python-Template/workflows/Lint%20and%20unit%20testing/badge.svg)

This template shows a basic usecase of an external adapter written in Python for the CryptoCompare API. It can be ran locally, in Docker, AWS Lambda, or GCP Functions.


## Run with Docker

Build the image

```
docker build . -t cl-ea
```

Run the container

```
docker run -it -p 8080:8080 cl-ea
```

Register image
```
python python3 register_image.py <path>
```

Score image
```
python python3 image_score.py <path>
```