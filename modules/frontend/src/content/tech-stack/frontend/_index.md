---
title: "Michal Skiba"
draft: false
type: "root"
---

# Frontend

## Stack

The user interface is built using [Hugo](https://gohugo.io/), a static site generator that allows me to focus on writing blog content in Markdown. I customize the UI with [Bootstrap](https://getbootstrap.com/), as well as my own [HTML](https://html.spec.whatwg.org/multipage/) and [CSS](https://www.w3.org/Style/CSS/Overview.en.html). I've utilized [JavaScript](https://www.javascript.com/) to bring additional functionality to the demo pages. The frontend is hosted locally using [Docker Compose](https://github.com/OAI/OpenAPI-Specification) and [nginx](https://nginx.org/), providing a consistent development environment.

## Architecture

Static site is stored on [AWS S3](https://aws.amazon.com/s3/) and hosted using [AWS CloudFront](https://aws.amazon.com/cloudfront/) for fast, cached, and reliable content delivery. This setup is fully serverless, ensuring scalability and cost-effectiveness.

![frontend_architecture.png class=arch-img](/frontend_architecture.svg)

## Deployment

I built a [Python](https://www.python.org/) script to streamline the deployment process. This script triggers a [Hugo](https://gohugo.io/) build to generate the static site and then uses [Boto3](https://pypi.org/project/boto3/) to upload the generated static site to an [AWS S3](https://aws.amazon.com/s3/) bucket. This automated approach ensures efficient and consistent deployment of the frontend.
