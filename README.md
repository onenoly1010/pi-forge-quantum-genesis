# Pi Forge Quantum Genesis

This project is a Flask-based web application that provides a simple health check endpoint.

## Setup

1.  **Install Python:** Make sure you have Python 3.11 or higher installed and added to your system's PATH.

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```

3.  **Activate the virtual environment:**
    -   On Windows:
        ```bash
        .\.venv\Scripts\Activate.ps1
        ```
    -   On macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r backend/requirements.txt
    ```

## Running the Application

To run the application, execute the following command:

```bash
python backend/app.py
```

The application will be available at `http://127.0.0.1:5000`.

### Health Check

You can check the health of the application by visiting `http://127.0.0.1:5000/health`.
