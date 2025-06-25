Repository for [michalskiba.dev](https://michalskiba.dev/) webpage which is a portfolio of [Michał Skiba](https://www.linkedin.com/in/michal-skiba-dev/).

# Bin scripts

## Prerequisites

- Install [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Install [Docker](https://docs.docker.com/get-docker/)
- Install [Python 3.12](https://www.python.org/downloads/release/python-3120/)
- Run `bin/init` to setup python virtual environment
- Run `bin/build` to build the app
- Run `bin/build_tests` to build tests
    - By default both frontend and api docker images for tests are created
    - You can pass one or more arguments to build specific docker images
        - `frontend`
        - `api`


## Run application locally

- Run `bin/run`
    - Local URL: http://localhost:8080

## Run lint checks

- Run `bin/run_lint_checks`
    - By default lint checks are run for each module
    - You can pass one or more arguments to run lint checks for specific modules
        - `frontend`
        - `auth`
        - `core`
        - `web_parameter_tampering`
        - `sql_injection`
        - `host_header_injection`

## Run tests

- Run `bin/run_tests`
    - By default tests are run for each module
    - You can pass one or more arguments to run tests for specific modules
        - `auth`
        - `core`
        - `web_parameter_tampering`
        - `sql_injection`
        - `host_header_injection`

## Update python packages

- Run `bin/build_requirements`

## Deploy application

- Create `.env.sso` file at the repository root with env variables for AWS SSO login
    - `REGION`
    - `ACCOUNT_ID`
    - `SSO_ROLE_NAME`
    - `SSO_START_URL`
- Create `.env.prod` file at the repository root with env variables for AWS CloudFormation stack parameters
    - `STACK_NAME`
    - `REGION`
    - `SUBDOMAIN`
    - `DOMAIN`
    - `CERTIFICATE_ARN`
        - ARN for certificate from AWS Certificate Manager which must be created manually in us-east-1
    - `AUTH_SECRET_KEY`
    - `HOST_HEADER_INJECTION_SECRET_KEY`
    - `SENTRY_DSN`
    - `ADMIN_API_KEY`
    - `NOTIFICATION_EMAIL`
- Run `bin/deploy`
    - By default script creates/updates AWS CloudFormation  stack and uploads built frontend static files
    - You can pass one or more arguments to create/update stack or upload static files only
        - `cf_stack`
        - `frontend`

# Modules

## Frontend
- Frontend application for the portfolio, blog and demos pages
- Repository Path: `/modules/frontend`
- URL paths:
    - `/`
        - portfolio
    - `/blog/`
        - blog
    - `/demo/demo/web-parameter-tampering/press`
        - Web Parameter Tampering demo
    - `/demo/sql-injection/`
        - SQL Injection demo
    - `/demo/host-header-injection/password-reset/initiate/`
        - Host Header Injection demo


## API Core Layer

- Shared module used by API modules
- Repository Path: `/modules/core`
- Features
    - Custom router for API on AWS API Gateway + AWS Lambda
    - Custom database manager for SQLite on AWS Lambda

## API

### Auth API
- Lambda authorizer function. Used by other APIs to authenticate requests
- Repository Path: `/modules/auth`
- URL paths
    - `/api/demo/auth/`
        Lambda authorizer endpoint
    - `/api/demo/auth/login`
        Authentication endpoint
    - `/api/demo/auth/logout`
        Logout endpoint

### Web Parameter Tampering API
- API demonstrating Web Parameter Tampering vulnerability with optional security controls
- Repository Path: `/modules/web_parameter_tampering`
- URL paths
    - `/api/demo/web-parameter-tampering/press-application`
        - Fetch user's press application

### SQL Injection API
- API demonstrating SQL Injection vulnerability with optional security controls
- Repository Path: `/modules/sql_injection`
- URL paths
    - `/api/demo/sql-injection/parcel-stores`
        - Fetch parcel stores


### Host Header Injection API
- API demonstrating Host Header Injection vulnerability with optional security controls
- Repository Path: `/modules/host_header_injection`
- URL paths
    - `/api/demo/host-header-injection/password-reset/initiate`
        - Initiate password reset flow
    - `/api/demo/host-header-injection/password-reset/complete`
        - Complete password reset flow

