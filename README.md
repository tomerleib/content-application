# content-application

A simple python application that connects to MySQL and displays the content.

## Configuration

* _Network access_: The application is exposed on port 8000, I've created a ClusterIP type service that exposing this port and Ingress rule which forward the traffic on port 80 and path /content to the application.

* _Configuration and envrionment varaibles_: I've mapped the RDS endpoint and the DB name to environment variables that stored inside a configMap type for easy management.

* _Secrets_: The application is using MySQL_USERNAME and MYSQL_PASSWORD to access the DB, instead of storing those two as environment variables or using native Kubernetes Secrets, I've decided to use AWS Secret Management with the webhook in order to inject the secrets directly and securely to the pod.
