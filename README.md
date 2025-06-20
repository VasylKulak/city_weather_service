# Weather Service API

A FastAPI-based application that provides weather information for a city using the OpenWeatherMap API. 
It leverages AWS S3 and DynamoDB for caching purposes.

### Prerequisites

Before setting up the project, make sure you have:

1. An AWS account
2. A user with the following AWS IAM permissions:
    - `AmazonDynamoDBFullAccess_v2`
    - `AmazonS3FullAccess`
3. An S3 bucket created in your preferred AWS region

### Installation

Follow these steps to set up and run the project:

```bash
# Clone the repository
git clone https://github.com/VasylKulak/city_weather_service
cd city_weather_service
```

### Set up environment variables

Create a .env file in the root directory based on .env.example. You need to specify the following environment variables:

```
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key

AWS_REGION=your_aws_region         # e.g. us-east-1
S3_BUCKET_NAME=your_s3_bucket_name

OPENWEATHER_MAP_API_KEY=your_openweather_map_api_key
```

## Run locally with Docker

```
#Build Docker image by running the followoing command in the project root directory
docker build -t fastapi-weather-app .

# Run the container
docker run -p 8000:8000 --env-file .env fastapi-weather-app
```

### API Documentation

After running the container, access the interactive Swagger docs at:

```
http://127.0.0.1:8000/docs/
```

## Deployment to AWS Elastic Beanstalk

To deploy this project on AWS Elastic Beanstalk (Python 3.12), follow these steps:

### 1. Prepare required files

The root of your project contains the following folder and files:

- `app/` directory — with your FastAPI application
- `requirements.txt` — Python dependencies
- `Procfile` — tells EB how to run your app

### 2. Create deployment ZIP archive

From the root of the project, run:

```bash
zip -r weather_app.zip app requirements.txt Procfile
```

Do not include .env — environment variables will be configured in the AWS Console.

### 3. Deploy using Elastic Beanstalk

- Go to [Elastic Beanstalk Console](https://console.aws.amazon.com/elasticbeanstalk/)
- Create a new **Python 3.12** environment
- Upload the `weather_app.zip` archive created earlier
- In **Configuration → Software → Environment properties**, add the same ENV variables that were
  used for running app locally.

### 4. Access your app

Once deployed, your FastAPI app will be available at:

```
http://<your-env>.elasticbeanstalk.com/docs
```

Use this URL to access the Swagger UI for your weather API.




