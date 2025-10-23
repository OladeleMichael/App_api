# FastAPI Social Media API

A robust REST API built with FastAPI that provides social media functionality including user authentication, post management, and voting/liking system. This API uses PostgreSQL for data persistence and JWT for secure authentication.

## Features

- **User Management**
  - User registration with secure password hashing
  - User authentication with JWT tokens
  - User profile retrieval

- **Post Management**
  - Create, read, update, and delete posts
  - Post ownership and authorization
  - Search and pagination support
  - Post visibility control

- **Voting System**
  - Like/unlike posts
  - Vote count tracking
  - User vote validation

- **Security**
  - JWT-based authentication
  - Password hashing with bcrypt
  - OAuth2 with Bearer tokens
  - Environment-based configuration

## Technology Stack

- **Framework**: FastAPI 0.89.1
- **Database**: PostgreSQL with SQLAlchemy 2.0.10
- **Authentication**: Python-JOSE, Passlib
- **Server**: Uvicorn with Gunicorn
- **Migrations**: Alembic 1.11.1
- **Validation**: Pydantic 1.10.6
- **Containerization**: Docker & Docker Compose

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)
- Docker (optional, for containerized deployment)

## Installation

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/OladeleMichael/App_api.git
   cd App_api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   - Install PostgreSQL if not already installed
   - Create a new database for the application

5. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_HOSTNAME=localhost
   DATABASE_PORT=5432
   DATABASE_PASSWORD=your_password
   DATABASE_NAME=your_database_name
   DATABASE_USERNAME=your_username
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

6. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

7. **Start the development server**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://127.0.0.1:8000`

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## API Endpoints

### Authentication
- `POST /login` - User login (returns JWT token)

### Users
- `POST /users/` - Create a new user
- `GET /users/{id}` - Get user by ID
- `GET /users/` - Get all users

### Posts
- `POST /posts/` - Create a new post (requires authentication)
- `GET /posts/` - Get all posts with vote counts (supports pagination and search)
- `GET /posts/{id}` - Get a specific post with vote count
- `PUT /posts/{id}` - Update a post (requires authentication and ownership)
- `DELETE /posts/{id}` - Delete a post (requires authentication and ownership)

### Votes
- `POST /vote/` - Vote on a post (like/unlike, requires authentication)

## Database Models

### User
- `id`: Integer (Primary Key)
- `firstname`: String
- `lastname`: String
- `email`: String (Unique)
- `password`: String (Hashed)
- `phone_number`: String
- `created_at`: Timestamp

### Post
- `id`: Integer (Primary Key)
- `title`: String
- `content`: String
- `published`: String (default: 'true')
- `created_at`: Timestamp
- `owner_id`: Integer (Foreign Key to User)

### Vote
- `user_id`: Integer (Primary Key, Foreign Key to User)
- `post_id`: Integer (Primary Key, Foreign Key to Post)

## Docker Deployment

### Using Docker Compose (Production)

1. **Build and run with Docker Compose**
   ```bash
   docker-compose -f docker-compose-prod.yml up -d
   ```

This will start:
- FastAPI application on port 80
- PostgreSQL database with persistent volume

### Using Dockerfile

1. **Build the Docker image**
   ```bash
   docker build -t fastapi-app .
   ```

2. **Run the container**
   ```bash
   docker run -d -p 8000:8000 --env-file .env fastapi-app
   ```

## Project Structure

```
App_api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── oauth2.py            # JWT authentication logic
│   ├── utils.py             # Utility functions (password hashing)
│   ├── customlogging.py     # Custom logging configuration
│   └── routers/
│       ├── auth.py          # Authentication routes
│       ├── user.py          # User management routes
│       ├── post.py          # Post management routes
│       └── vote.py          # Voting routes
├── alembic/                 # Database migration files
├── Dockerfile               # Docker configuration
├── docker-compose-prod.yml  # Production Docker Compose
├── requirements.txt         # Python dependencies
├── alembic.ini             # Alembic configuration
└── README.md               # This file
```

## Configuration

The application uses environment variables for configuration. All settings are validated using Pydantic's `BaseSettings` class in `app/config.py`.

Required environment variables:
- `DATABASE_HOSTNAME`: PostgreSQL host
- `DATABASE_PORT`: PostgreSQL port
- `DATABASE_PASSWORD`: Database password
- `DATABASE_NAME`: Database name
- `DATABASE_USERNAME`: Database username
- `SECRET_KEY`: Secret key for JWT encoding
- `ALGORITHM`: Algorithm for JWT (e.g., HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

## Authentication Flow

1. User registers via `POST /users/`
2. User logs in via `POST /login` with email and password
3. API returns a JWT access token
4. Client includes token in `Authorization: Bearer <token>` header for protected endpoints
5. Server validates token and extracts user information

## CORS Configuration

The API is configured to accept requests from all origins (`origins = ["*"]`). For production, update the `origins` list in `app/main.py` to include only your frontend domain.

## Production Deployment

For production deployment using Gunicorn:

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

The repository includes a `gunicorn.service` file for systemd service configuration.

## Development

### Running in Development Mode
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Creating Database Migrations
```bash
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is available for educational and personal use.

## Author

Michael Oladele

## Acknowledgments

- FastAPI documentation
- SQLAlchemy documentation
- Alembic migration tool