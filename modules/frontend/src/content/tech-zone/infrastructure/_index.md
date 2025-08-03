---
title: "Michal Skiba"
draft: false
type: "root"
---

# Infrastructure

SAM/CloudFormation Template: [link](https://github.com/dev-michal-skiba/michalskiba-dev/blob/master/template.yaml)

## DNS

The domain `michalskiba.dev` is registered via Squarespace. DNS is managed in an Amazon Route 53 Hosted Zone, which acts as the authoritative nameserver for the domain. In this hosted zone, an Alias A record is configured for the root domain and an Alias CNAME record is configured for the `www` subdomain. Both of these DNS records are set up in Route 53 to point to the same Amazon CloudFront distribution, which serves the website content globally.


![tech-zone/infra/dns.png class=arch-img](/tech-zone/infra/dns.svg)

## Content Delivery

The architecture is designed to efficiently serve both static content and dynamic API requests. User requests are first routed through Amazon CloudFront, which acts as a global CDN. The default origin for CloudFront points to Amazon S3 and is globally cached, ensuring fast delivery of static assets. For API requests, CloudFront forwards traffic to Amazon API Gateway at the `/api` path, which is configured as a non-cached origin to ensure dynamic responses. API Gateway then routes requests to various AWS Lambda functions, each implementing a different security demo. Some demos are protected by a Lambda Authorizer to provide authorization capabilities when required.


![tech-zone/infra/api.png class=arch-img](/tech-zone/infra/api.svg)

## Telemetry

The telemetry system is designed to provide visibility into both expected and administrative activity across the web attack demos featured on the site. Each time an exploit is triggered — whether by a user exploring the demo or by an admin for testing purposes — the event is logged by the relevant AWS Lambda function to a shared AWS CloudWatch log group. CloudWatch metric filters process these logs and distinguish between user and admin exploits using a secret stored in local storage for admin sessions. All exploit events are published as custom metrics in CloudWatch and visualized in a unified CloudWatch dashboard, alongside API usage data from the API Gateway log group, to provide a comprehensive view of site activity. While user exploits are an anticipated part of the interactive demos, CloudWatch alarms are configured to track their occurrence and send notifications to admin via email through an Amazon SNS topic, ensuring I am aware of ongoing usage.


![tech-zone/infra/telemetry.png class=arch-img](/tech-zone/infra/telemetry.svg)
