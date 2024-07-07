---
title: "Michal Skiba"
draft: false
type: "root"
---

## About Me

I am a dedicated computer science enthusiast with solid experience in developing backend of web applications. My true
passion lies in the world of Python programming, but I am always eager to expand my skill set and take new and exciting
challenges. In my free time, I am constantly exploring and experimenting with new areas of computer science that
interest me.

---

## Idea behind the page

I have developed an interest in web application security, a field that fascinates me for its complexity and the critical
role it plays in protecting digital assets. To delve deeper into this area, I created this portfolio blog as a platform
to share my experiments and projects related to web security. Through this blog, I showcase a series of live demo
projects that illustrate popular web attacks and the techniques used to mitigate them. Each project is designed to
provide practical, hands-on examples of web vulnerabilities and defenses, reflecting my ongoing exploration of this
exciting domain. Feel free to explore my work and see how I am applying my skills to tackle real-world security
challenges.

---

## Frontend

##### Stack

The user interface is built using [Hugo](https://gohugo.io/), a static site generator that allows me to focus on writing
blog content in Markdown. I customize the UI with [Bootstrap](https://getbootstrap.com/), as well as my own
[HTML](https://html.spec.whatwg.org/multipage/) and [CSS](https://www.w3.org/Style/CSS/Overview.en.html). For the demo
pages, I have also developed some [JavaScript](https://www.javascript.com/) code. The frontend is hosted locally using
[Docker Compose](https://github.com/OAI/OpenAPI-Specification), providing a consistent development environment.

##### Architecture

Built static site is stored on [AWS S3](https://aws.amazon.com/s3/) and hosted using
[AWS CloudFront](https://aws.amazon.com/cloudfront/) for fast and reliable content delivery.

![frontend_architecture.png class=arch-img](/frontend_architecture.png)

##### Deployment

I built a [Python](https://www.python.org/) script to streamline the deployment process. This script triggers a
[Hugo](https://gohugo.io/) build to generate the static site and then uses [Boto3](https://pypi.org/project/boto3/) to
upload the generated static site to an [AWS S3](https://aws.amazon.com/s3/) bucket. This automated approach ensures
efficient and consistent deployment of the frontend.

---

## Backend

##### Stack

The backend is powered by [Python](https://www.python.org/), using [SQLite](https://www.sqlite.org/) for database
management and the [Peewee](https://pypi.org/project/peewee/) library for ORM (Object-Relational Mapping). This setup is
designed specifically for demo purposes, providing a robust and efficient way to handle data and server-side logic. The
API is locally hosted using [AWS SAM](https://aws.amazon.com/serverless/sam/), providing a consistent development
environment.

##### Architecture

The backend architecture is defined in an [AWS SAM](https://aws.amazon.com/serverless/sam/) template and utilizes
[AWS API Gateway](https://aws.amazon.com/api-gateway/) and [AWS Lambda](https://aws.amazon.com/lambda/) to provide a
scalable API solution. [AWS API Gateway](https://aws.amazon.com/api-gateway/) manages API endpoints, while separate
[AWS Lambda](https://aws.amazon.com/lambda/) functions handle different endpoints and business logic. This serverless
setup ensures efficient, scalable, and cost-effective backend.

![backend_architecture.png class=arch-img](/backend_architecture.png)

##### Deployment

The backend is deployed using [AWS SAM](https://aws.amazon.com/serverless/sam/), which automates the packaging and
deployment of serverless resources like [AWS API Gateway](https://aws.amazon.com/api-gateway/) and
[AWS Lambda](https://aws.amazon.com/lambda/). SAM CLI commands manage the deployment process, ensuring a consistent and
efficient setup for backend services.
