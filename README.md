# docktier

This project demonstrates orchestration between Docker containers, with a focus on integrating a Flask application and a Vaultgres service.

## Project Structure

- `docker-compose.yml` — Orchestrates the services (Flask app, Vaultgres, etc.)
- `Dockerfile` — Builds the Flask app container
- `Makefile` — Common commands for building and running the project
- `src/` — Source code for the Flask application

## Prerequisites

- Docker
- Docker Compose
- [Vaultgres](https://github.com/heshamkhaledd/vaultgres) (must be cloned and run by Docker before starting this project)
    - All vaultgres prerequisites are considered here as well.

## Setup

1. **Clone Vaultgres**

   ```bash
   git clone https://github.com/heshamkhaledd/vaultgres.git
   cd vaultgres
   make
   ```

2. **Clone and Run This Project**

   ```bash
   git clone https://github.com/heshamkhaledd/dockertier.git
   cd docktier
   make
   ```
