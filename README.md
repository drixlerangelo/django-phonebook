# Phonebook
A phonebook application using the Django Rest Framework.

## Requirements
- [Docker](https://docker.com)

## Setup

### For NON-PRODUCTION environment

1. Run the following command:
```
cp .env.example .env
```

2. In your Dotenv file, change the following variables:
```
APP_ENV=development
APP_DEBUG=1
```

3. You can run the following command to add all the services to your project.
```
docker-compose up -d --build
```

### For PRODUCTION environment

1. Run the following command:
```
cp .env.example .env
```

2. You can run the following command to add all the services to your project.
```
docker-compose up -d --build
```
