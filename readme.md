# Transfer Listener

This Django application connects to the Ethereum mainnet via Infura, listens for transfer events of BAYC, saves the events in a SQLite database, and has an API endpoint to retrieve the transfer events data for a token ID.

## Table of Contents

- [Environment Variables](#environment-variables)
- [Installation](#installation)
- [Usage](#usage)
- [Test](#test)

## Environment Variables

- Copy .env.sample and replace values

## Installation (Linux)

- Create and activate virtualenv
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

- Install packages
    ```bash
    pip install -r requirements.txt
    ```

- Migrate DB
    ```bash
    python manage.py migrate
    ```

## Usage

- Run the Listener
    ```bash
    python manage.py listen_transfers
    ```

- Run the Django server
    ```bash
    python manage.py runserver
    ```

## Test

```bash
http://127.0.0.1:8000/bayc/history/<token_id>/
```