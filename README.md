Repository for [michalskiba.dev](https://www.michalskiba.dev/) webpage which is a portfolio of Michał Skiba.

# How to run

- Install [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Install [Docker](https://docs.docker.com/get-docker/)
- Run `./bin/build` to build the project
- Run `./bin/run` to run the project locally

# Modules

## Frontend
- Path: `/modules/frontend/`
- Local URL: http://localhost:8080
- Frontend application for the portfolio, blog and demos pages.

## Auth API
- Path: `/modules/auth/`
- Local URL: http://api.localhost:8080/demo/auth
- Lambda authorizer function. Used by other APIs to authorize requests.

## SQL Injection API
- Path: `/modules/sql_injection/`
- Local URL: http://api.localhost:8080/demo/sql-injection
- Lambda function that provides an API that is vulnerable or not to SQL Injection depending on the request query parameter.

## Web Parameter Tampering API
- Path: `/modules/web_parameter_tampering/`
- Local URL: http://api.localhost:8080/demo/web-parameter-tampering
- Lambda function that provides an API that is vulnerable or not to Web Parameter Tampering depending on the request query parameter.

## Host Header Injection API
- Path: `/modules/host_header_injection/`
- Local URL: http://api.localhost:8080/demo/host-header-injection
- Lambda function that provides an API that is vulnerable or not to Host Header Injection depending on the request headers.
