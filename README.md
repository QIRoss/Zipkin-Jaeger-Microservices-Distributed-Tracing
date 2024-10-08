# Zipkin/Jaeger Microservices Distributed Tracing

Studies based in day 63-64 of 100 Days System Design for DevOps and Cloud Engineers.

https://deoshankar.medium.com/100-days-system-design-for-devops-and-cloud-engineers-18af7a80bc6f

Days 61–70: Advanced Observability and Analytics

Day 63–64: Implement distributed tracing at scale using tools like Zipkin or Jaeger in a complex microservices environment.

## Project Overview

## Project Overview

This project demonstrates the implementation of distributed tracing in a microservices environment using **OpenTelemetry**, **Zipkin**, and **Jaeger**.

### Key Technologies

- **Zipkin**: Zipkin is a distributed tracing system that helps gather timing data needed to troubleshoot latency problems in microservice architectures. It collects and records trace data, providing visibility into the path and timing of requests within and between services.

- **Jaeger**: Jaeger is an open-source distributed tracing system developed by Uber. It is used for monitoring and troubleshooting microservices-based distributed systems, supporting functions such as root cause analysis and service dependency analysis.

- **OpenTelemetry**: OpenTelemetry is an observability framework for cloud-native software that provides a collection of APIs and tools for generating, collecting, and exporting traces, metrics, and logs. In this project, OpenTelemetry is used to instrument FastAPI services, enabling the trace data to be sent to either Zipkin or Jaeger.

### Docker Setup

The project consists of three FastAPI microservices: **user_service**, **order_service**, and **payment_service**. These services are instrumented with OpenTelemetry for distributed tracing. The tracing data is sent to **Zipkin** or **Jaeger**, depending on the service configuration.

### Running the Project

1. Clone this repository and navigate to the project directory.
2. Build and run the containers using Docker Compose:

```
docker-compose up --build
```

This will build the Docker images for the microservices and start the following containers:

* user_service: Running on port 8001
* order_service: Running on port 8002
* payment_service: Running on port 8003
* Zipkin: Running on port 9411
* Jaeger: Running on port 16686 for the UI and 14250 for the collector.

### Accessing the Services
* Zipkin: After starting the services, Zipkin will be available at ```http://localhost:9411```. You can use the Zipkin UI to view and search traces from the microservices.

* Jaeger: After starting the services, Jaeger will be available at ```http://localhost:16686```. This will let you analyze distributed traces from the services configured to send tracing data to Jaeger.

### Testing the Microservices
You can test the microservices using curl commands as follows:
* Create a user in user_service:
```
curl -X POST "http://localhost:8001/register/" -H "Content-Type: application/json" -d '{"username": "john_doe", "email": "john@example.com"}'
```
* Get user profile from user_service:
```
curl -X GET "http://localhost:8001/profile/1"
```
* Create an order in order_service:
```
curl -X POST "http://localhost:8002/order/" -H "Content-Type: application/json" -d '{"user_id": 1, "item_name": "Laptop", "quantity": 2}'
```
* curl -X GET "http://localhost:8002/order/67047d3bb70d6e7e36f5ae34":
```
curl -X GET "http://localhost:8002/order/67047d3bb70d6e7e36f5ae34"
```
* Process a payment in payment_service:
```
curl -X POST "http://localhost:8003/payment/" -H "Content-Type: application/json" -d '{"user_id": 1, "order_id": 1, "amount": 1000}'
```
* Get payment details from payment_service:
```
curl -X GET "http://localhost:8003/payment/1"
```

## Author
This project was implemented by [Lucas de Queiroz dos Reis][2]. It is based on the Day 23–24: Automate multi-environment setups using Terraform and Ansible dynamic inventories from the [100 Days System Design for DevOps and Cloud Engineers][1].

[1]: https://deoshankar.medium.com/100-days-system-design-for-devops-and-cloud-engineers-18af7a80bc6f "Medium - Deo Shankar 100 Days"
[2]: https://www.linkedin.com/in/lucas-de-queiroz/ "LinkedIn - Lucas de Queiroz"