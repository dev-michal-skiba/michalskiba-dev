---
title: "Michal Skiba"
draft: false
type: "root"
---

# Stack

The backend is powered by [Python](https://www.python.org/), using [SQLite](https://www.sqlite.org/) for database
management and the [Peewee](https://pypi.org/project/peewee/) library for ORM (Object-Relational Mapping). This setup is
designed specifically for demo purposes, providing a robust and efficient way to handle data and server-side logic. The
API is locally hosted using [AWS SAM](https://aws.amazon.com/serverless/sam/), providing a consistent development
environment.

# Architecture

The backend architecture is defined in an [AWS SAM](https://aws.amazon.com/serverless/sam/) template and utilizes
[AWS API Gateway](https://aws.amazon.com/api-gateway/) and [AWS Lambda](https://aws.amazon.com/lambda/) to provide a
scalable API solution. [AWS API Gateway](https://aws.amazon.com/api-gateway/) manages API endpoints, while separate
[AWS Lambda](https://aws.amazon.com/lambda/) functions handle different endpoints and business logic. This serverless
setup ensures efficient, scalable, and cost-effective backend.

![backend_architecture.png class=arch-img](/backend_architecture.png)

# Deployment

The backend is deployed using [AWS SAM](https://aws.amazon.com/serverless/sam/), which automates the packaging and
deployment of serverless resources like [AWS API Gateway](https://aws.amazon.com/api-gateway/) and
[AWS Lambda](https://aws.amazon.com/lambda/). SAM CLI commands manage the deployment process, ensuring a consistent and
efficient setup for backend services.
