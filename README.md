Repository for [michalskiba.dev](https://www.michalskiba.dev/) webpage which is a portfolio of Michał Skiba.

# How to run

- Install [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Run `./bin/build` to build the project
- Run `./bin/start` to start the project locally

# Modules

## Frontend
- Path: `/modules/frontend/`
- Local URL: http://localhost:1313
- Frontend application for the portfolio, blog and demos pages.

## Auth API
- Path: `/modules/auth/`
- Local URL: http://localhost:3000/demo/auth
- Lambda authorizer function. Used by other APIs to authorize requests.

## SQL Injection API
- Path: `/modules/sql_injection/`
- Local URL: http://localhost:3000/demo/sql-injection
- Lambda function that provides an API that is vulnerable or not to SQL Injection depending on the request query parameter.

## Web Parameter Tampering API
- Path: `/modules/web_parameter_tampering/`
- Local URL: http://localhost:3000/demo/web-parameter-tampering
- Lambda function that provides an API that is vulnerable or not to Web Parameter Tampering depending on the request query parameter.
