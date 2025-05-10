# Django MCP E-commerce

This is a Django implementation of a Model Context Protocol (MCP) for an e-commerce application.

Django E-Commercial Model Context Protocol (MCP) Playground Welcome to the MCP Playground – where your Django app becomes best friends with your LLM. It’s an open protocol that lets your large language model tap into real-time data and external tools like it’s been doing it all its life.g

## Setup

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r ./requirements.txt
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Run the development server:
```bash
python manage.py runserver 0.0.0.0:8000
```

6. Run the MCP Server
cd mcp_order_server
mcp dev mcp_server.py

## API Endpoints



## Features

- RESTful API for product management
- Model Context Protocol implementation
- Product recommendation system (basic implementation)
- CORS enabled for frontend integration

## Frontend Integration

The API can be integrated with any frontend framework. The endpoints are CORS-enabled for easy integration. 


