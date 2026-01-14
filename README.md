# Digital Key Backend API

A FastAPI-based backend service for managing digital keys with cloud storage integration. This project provides secure REST APIs for uploading, managing, and retrieving digital keys.

## Features

- ✅ Digital key upload & management
- ✅ Cloud storage integration
- ✅ Secure REST APIs
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ Request/response validation with Pydantic schemas
- ✅ Organized project structure with separation of concerns

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.8+
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Server**: Uvicorn
- **Cloud Storage**: Cloud storage integration

## Project Structure

```
digital-key-backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── digital_key.py      # API routes
│   ├── core/
│   │   └── config.py               # Configuration settings
│   ├── db/
│   │   └── database.py             # Database setup
│   ├── models/
│   │   └── digital_key.py          # SQLAlchemy models
│   ├── schemas/
│   │   └── digital_key.py          # Pydantic schemas
│   ├── services/
│   │   └── digital_key_service.py  # Business logic
│   ├── utils/
│   │   └── cloud.py                # Cloud storage utilities
│   └── main.py                     # Application entry point
├── requirements.txt
└── README.md
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd digital-key-backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The database configuration is defined in `app/core/config.py`. By default, it uses SQLite:

```python
DATABASE_URL = "sqlite:///./digital_key.db"
```

## Run Locally

Start the development server with:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Interactive API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Digital Keys

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/digital-keys/` | Create a new digital key |
| `GET` | `/api/v1/digital-keys/` | Retrieve all digital keys |
| `GET` | `/api/v1/digital-keys/{key_id}` | Retrieve a specific digital key |
| `PUT` | `/api/v1/digital-keys/{key_id}` | Update a digital key |
| `DELETE` | `/api/v1/digital-keys/{key_id}` | Delete a digital key |

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Check API health status |

## Example Usage

### Create a Digital Key

```bash
curl -X POST "http://localhost:8000/api/v1/digital-keys/" \
  -H "Content-Type: application/json" \
  -d '{
    "key_name": "my_key",
    "key_value": "secret_value_123",
    "owner": "user@example.com"
  }'
```

### Get All Digital Keys

```bash
curl "http://localhost:8000/api/v1/digital-keys/"
```

### Get a Specific Digital Key

```bash
curl "http://localhost:8000/api/v1/digital-keys/1"
```

## Database Schema

The `digital_keys` table has the following structure:

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | Integer | Primary Key, Auto-increment |
| `key_name` | String | Unique, Not Null, Indexed |
| `key_value` | String | Unique, Not Null, Indexed |
| `owner` | String | Not Null, Indexed |

## Development

### Adding New Features

1. Create models in `app/models/`
2. Define schemas in `app/schemas/`
3. Implement business logic in `app/services/`
4. Create API routes in `app/api/v1/`

### Dependencies

All required packages are listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Security Considerations

⚠️ **Note**: For production use:

- Implement proper authentication and authorization
- Use environment variables for sensitive configuration
- Enable HTTPS/TLS
- Implement rate limiting
- Add input validation and sanitization
- Use proper error handling without exposing internal details
- Implement logging and monitoring

## Future Enhancements

- [ ] User authentication and authorization
- [ ] Advanced cloud storage integration (AWS S3, Azure Blob Storage)
- [ ] Key encryption and decryption
- [ ] Audit logging
- [ ] API rate limiting
- [ ] Unit and integration tests
- [ ] Docker containerization
- [ ] CI/CD pipeline

## License

[Add your license here]

## Support

For issues and questions, please create an issue in the repository.