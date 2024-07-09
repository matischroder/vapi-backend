## Installation Instructions

To set up the project environment and install the necessary dependencies, follow the steps below based on your operating system.

### Prerequisites

- Ensure you have Python 3.6 or higher installed.
- Install `pip` (Python package installer) if it is not already installed.
- Install `virtualenv` for creating isolated Python environments.

### Setup Instructions

#### 1. Clone the Repository

```sh
git clone https://https://github.com/matischroder/vapi-intergration.git
cd vapi-intergration
```

#### 2. Create a Virtual Environment

Create a virtual environment to isolate the project dependencies.

```sh
python -m venv venv
```

#### 3. Activate the Virtual Environment

- **On macOS/Linux:**

  ```sh
  source venv/bin/activate
  ```

- **On Windows:**

  ```sh
  venv\Scripts\activate
  ```

#### 4. Install `pip-tools`

Install `pip-tools` to manage the dependencies.

```sh
pip install pip-tools
```

#### 5. Generate `requirements.txt`

Generate the `requirements.txt` file from `requirements.in`.

```sh
pip-compile requirements.in
```

#### 6. Install Dependencies

Install all the dependencies listed in `requirements.txt`.

```sh
pip install -r requirements.txt
```

### Additional Information

- **Updating Dependencies:** To add new packages and update `requirements.in` and `requirements.txt`, use the provided `install.sh` script.

  ```sh
  ./install.sh package1 package2 ...
  ```

- **Environment Variables:** Ensure you have a `.env` file in the root directory with the required environment variables.

### Example `.env` File

```ini
export PORT=5050
export CORS_ORIGIN='["http://localhost","http://localhost:3000","https://yourdomain.com","*"]'
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_REGION=
export VAPI_API_KEY=
export VAPI_PUBLIC_KEY=
```

### Running the Application

After setting up the environment and installing dependencies, you can run the application using:

```sh
python run.py
```

### Cleaning Up

To deactivate the virtual environment:

```sh
deactivate
```
