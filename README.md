# The Cryptwell Castle Resort - Backend

## Project Overview
The Cryptwell Castle Resort backend serves as the backbone of the application, managing all critical data operations and providing a seamless API for the frontend. It handles:
- User authentication and management.
- Room and reservation data.
- Integration with a PostgreSQL database hosted on AWS.
- Securely managing data between the frontend and database through RESTful API endpoints.

### Key Features
- **Authentication**: Register and authenticate users securely.
- **Reservation Management**: Handle room availability and user bookings.
- **Room Data**: Fetch data on themed rooms and wings.
- **Seamless Frontend Integration**: Exposes a robust API to power the immersive frontend experience.

---

## Technology Stack
The backend leverages the following technologies:
- **Python**: For scalable and efficient server-side development.
- **Django**: As the web framework for building the REST API.
- **PostgreSQL**: As the relational database to store all application data.
- **Docker**: For containerizing the backend application.
- **Terraform**: For infrastructure as code, managing AWS resources.
- **AWS**:
  - **EC2**: For hosting the Django application.
  - **RDS**: For the PostgreSQL database.
  - **S3**: For storing site images.
  - **Route 53**: For custom domain management.
  - **ECS**: For deploying Docker containers.

---

## Features
- **User Authentication**: Secure registration and login functionality.
- **Reservation System**: Robust handling of room bookings and availability.
- **Wing Data**: Organized endpoints for querying details about the hotel wings.
- **Data Validation**: Ensures consistency and integrity of data operations.

---

## Setup and Installation

### Prerequisites
- **Python** (3.8 or higher)
- **Docker** (latest version)
- **Django** (as specified in `requirements.txt`)

### Steps to Run Locally
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/brennambond/cryptwellcastleresort_backend.git
   cd hh_api
   ```

2. **Set Up Docker**:
   - Build and start the Docker container:
     ```bash
     docker compose build
     docker compose up
     ```

3. **Activate the Virtual Environment** (if needed outside Docker):
   ```bash
   source venv/Scripts/activate
   ```
   To deactivate:
   ```bash
   deactivate
   ```

4. **Run Migrations**:
   Ensure the database schema is up to date:
   ```bash
   ./manage.py makemigrations
   ./manage.py migrate
   ```

5. **Start the Development Server**:
   - If not using Docker:
     ```bash
     python manage.py runserver
     ```

---

## Usage
The backend provides several key API endpoints:
- **Rooms API**:
  - `GET /api/rooms/`: Fetches all available rooms.
  - `GET /api/rooms/wings/`: Retrieves details about the four themed wings.
- **Authentication API**:
  - `POST /api/auth/register/`: Registers a new user.

### Notes:
- Use `https://hauntedhotel-backend-api.com/` for HTTPS requests.
- Use `http://35.170.218.30/` for HTTP requests.

---

## Deployment
The backend is deployed on AWS using the following setup:
- **Docker** containerizes the Django application.
- **ECS** runs the containers.
- **Terraform** provisions AWS resources:
  - EC2 instance for hosting the application.
  - RDS for PostgreSQL database management.
  - S3 bucket for image storage.
  - Route 53 for custom domain management.
  
---

## Contributing
This project is a personal endeavor and does not accept external contributions.

---

## License
This project is licensed under the **MIT License**, granting users the freedom to explore the code within the terms of this license.

---

## Contact
For questions or assistance, please contact me at:
- **Email**: [brennambond@gmail.com](mailto:brennambond@gmail.com)

---

Thank you for supporting The Cryptwell Castle Resort project—may your experience be delightfully chilling!
