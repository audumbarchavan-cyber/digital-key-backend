# Digital Key Backend API

A comprehensive FastAPI-based backend service for managing digital keys, users, machines, and access permissions with local cloud storage integration. This project provides secure REST APIs for managing credentials and controlling machine access.

## Features

### Core Features
- ✅ Digital key upload & management with automatic cloud backup
- ✅ User management with role-based access control (RBAC)
- ✅ Machine registration and management
- ✅ Fine-grained permission control and access management
- ✅ Digital key-based access control for machines
- ✅ Secure REST APIs with validation

### Advanced Features
- ✅ Local cloud storage integration for backups
- ✅ Audit trails with timestamps
- ✅ Access revocation and history tracking
- ✅ User access summaries and reporting
- ✅ Machine access summaries and reporting
- ✅ Active/inactive status management
- ✅ CRUD operations with error handling

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.8+
- **Database**: SQLite with SQLAlchemy ORM
- **Validation**: Pydantic schemas
- **Server**: Uvicorn
- **Storage**: Local file-based cloud storage

## Project Structure

```
digital-key-backend/
├── app/
│   ├── api/v1/
│   │   ├── digital_key.py          # Digital key endpoints
│   │   ├── users.py                # User management endpoints
│   │   ├── machines.py             # Machine management endpoints
│   │   └── permissions.py          # Permission management endpoints
│   ├── core/
│   │   └── config.py               # Configuration & settings
│   ├── db/
│   │   └── database.py             # Database setup & connection
│   ├── models/
│   │   ├── digital_key.py          # Digital key model
│   │   ├── user.py                 # User model
│   │   ├── machine.py              # Machine model
│   │   └── permission.py           # Permission model
│   ├── schemas/
│   │   ├── digital_key.py          # Digital key schemas
│   │   ├── user.py                 # User schemas
│   │   ├── permission.py           # Machine & permission schemas
│   │   └── access.py               # Access summary schemas
│   ├── services/
│   │   ├── digital_key_service.py  # Digital key business logic
│   │   ├── user_service.py         # User business logic
│   │   ├── machine_service.py      # Machine business logic
│   │   └── permission_service.py   # Permission business logic
│   ├── utils/
│   │   └── cloud.py                # Cloud storage utilities
│   └── main.py                     # Application entry point
├── local_storage/                  # Local cloud storage (created at runtime)
├── requirements.txt
└── README.md
```

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

## API Endpoints Overview

### Digital Keys (7 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/digital-keys/` | Create a new digital key |
| `GET` | `/api/v1/digital-keys/` | Retrieve all digital keys |
| `GET` | `/api/v1/digital-keys/{key_id}` | Retrieve a specific digital key |
| `PUT` | `/api/v1/digital-keys/{key_id}` | Update a digital key |
| `DELETE` | `/api/v1/digital-keys/{key_id}` | Delete a digital key |
| `GET` | `/api/v1/digital-keys/cloud/uploads/list` | List cloud backups |
| `GET` | `/api/v1/digital-keys/cloud/download/{id}/{name}` | Download backup |

### Users (6 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/users/` | Create a new user |
| `GET` | `/api/v1/users/` | List all users |
| `GET` | `/api/v1/users/{user_id}` | Get user by ID |
| `GET` | `/api/v1/users/username/{username}` | Get user by username |
| `PUT` | `/api/v1/users/{user_id}` | Update user |
| `DELETE` | `/api/v1/users/{user_id}` | Delete user |

### Machines (8 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/machines/` | Create a new machine |
| `GET` | `/api/v1/machines/` | List all machines |
| `GET` | `/api/v1/machines/{machine_id}` | Get machine by ID |
| `GET` | `/api/v1/machines/name/{machine_name}` | Get machine by name |
| `GET` | `/api/v1/machines/type/{machine_type}` | Filter machines by type |
| `GET` | `/api/v1/machines/active/` | Get active machines only |
| `PUT` | `/api/v1/machines/{machine_id}` | Update machine |
| `DELETE` | `/api/v1/machines/{machine_id}` | Delete machine |

### Permissions (12 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/permissions/grant` | Grant user access to machine |
| `GET` | `/api/v1/permissions/` | List all permissions |
| `GET` | `/api/v1/permissions/{permission_id}` | Get permission by ID |
| `GET` | `/api/v1/permissions/user/{user_id}` | Get user's permissions |
| `GET` | `/api/v1/permissions/machine/{machine_id}` | Get machine's permissions |
| `GET` | `/api/v1/permissions/user/{user_id}/machine/{machine_id}` | Get specific permission |
| `PUT` | `/api/v1/permissions/{permission_id}` | Update permission |
| `POST` | `/api/v1/permissions/{permission_id}/revoke` | Revoke permission |
| `POST` | `/api/v1/permissions/user/{user_id}/machine/{machine_id}/revoke` | Revoke user's access |
| `DELETE` | `/api/v1/permissions/{permission_id}` | Delete permission record |
| `GET` | `/api/v1/permissions/access/user/{user_id}` | User's access summary |
| `GET` | `/api/v1/permissions/access/machine/{machine_id}` | Machine's access summary |

### Health Check (1 endpoint)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Check API health status |

**Total: 34 API endpoints**

## Example Usage

### Create a User

```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_operator",
    "user_type": "operator",
    "email": "john@company.com"
  }'
```

### Create a Machine

```bash
curl -X POST "http://localhost:8000/api/v1/machines/" \
  -H "Content-Type: application/json" \
  -d '{
    "machine_name": "prod-server-01",
    "machine_type": "server",
    "ip_address": "192.168.1.100",
    "description": "Production application server"
  }'
```

### Grant User Access to Machine

```bash
curl -X POST "http://localhost:8000/api/v1/permissions/grant" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "machine_id": 1,
    "digital_key_id": 1,
    "permission_level": "write"
  }'
```

### Get User's Access to Machines

```bash
curl "http://localhost:8000/api/v1/permissions/access/user/1"
```

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

## Documentation

Comprehensive documentation for specific features is provided through inline code documentation and API docs:

- **Swagger UI**: Visit `http://localhost:8000/docs` for interactive API documentation
- **ReDoc**: Visit `http://localhost:8000/redoc` for detailed API reference

## Key Components

### User Management
- Role-based access control with 4 user types: Admin, User, Operator, Viewer
- User creation, update, deletion, and retrieval
- Email and username uniqueness validation
- Audit timestamps (created_at, updated_at)

### Machine Management
- Machine registration with 6 machine types: Server, Workstation, IoT Device, Database, Storage, Other
- IP address and description tracking
- Active/inactive status management
- Machine type filtering and searching

### Permission System
- Grant/revoke user access to machines using digital keys
- 4 permission levels: Read, Write, Execute, Admin
- Permission active/inactive tracking
- Revocation with timestamp recording
- Prevents duplicate permissions

### Local Cloud Storage
- Automatic backup of digital keys
- User and machine data backup capability
- Metadata index for tracking backups
- JSON-based storage for easy inspection
- Configurable storage path via environment variable

## Database Models

### Users Table
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username VARCHAR UNIQUE NOT NULL,
  user_type VARCHAR NOT NULL,
  email VARCHAR UNIQUE NOT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);
```

### Machines Table
```sql
CREATE TABLE machines (
  id INTEGER PRIMARY KEY,
  machine_name VARCHAR UNIQUE NOT NULL,
  machine_type VARCHAR NOT NULL,
  ip_address VARCHAR,
  description VARCHAR,
  is_active INTEGER NOT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);
```

### Permissions Table
```sql
CREATE TABLE user_machine_permissions (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  machine_id INTEGER NOT NULL,
  digital_key_id INTEGER NOT NULL,
  permission_level VARCHAR NOT NULL,
  is_active BOOLEAN NOT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  revoked_at DATETIME,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (machine_id) REFERENCES machines(id),
  FOREIGN KEY (digital_key_id) REFERENCES digital_keys(id)
);
```

## Configuration

### Database
```python
# app/core/config.py
DATABASE_URL = "sqlite:///./digital_key.db"
```

### Cloud Storage
```python
# app/core/config.py
LOCAL_STORAGE_PATH = os.getenv("LOCAL_STORAGE_PATH", "./local_storage")
STORAGE_BUCKET_NAME = "digital-keys"
```

Set custom storage path via environment variable:
```bash
set LOCAL_STORAGE_PATH=C:\custom\path\to\storage
```

## Development

### Run Tests

You can test the API using curl commands or the interactive Swagger UI:

```bash
# Example: Create a user
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","user_type":"operator","email":"test@example.com"}'
```

### View API Documentation

- **Swagger UI**: Visit `http://localhost:8000/docs`
- **ReDoc**: Visit `http://localhost:8000/redoc`

## Dependencies

Main dependencies (see requirements.txt for full list):

- **fastapi** - Modern web framework
- **uvicorn** - ASGI server
- **sqlalchemy** - ORM database toolkit
- **pydantic** - Data validation
- **python-multipart** - File upload support

## Architecture

```
┌─────────────────────────────────────────────┐
│         FastAPI Application                 │
├─────────────────────────────────────────────┤
│ API Layer                                   │
│ ├─ Digital Key Endpoints                   │
│ ├─ User Endpoints                          │
│ ├─ Machine Endpoints                       │
│ └─ Permission Endpoints                    │
├─────────────────────────────────────────────┤
│ Service Layer (Business Logic)              │
│ ├─ digital_key_service                     │
│ ├─ user_service                            │
│ ├─ machine_service                         │
│ └─ permission_service                      │
├─────────────────────────────────────────────┤
│ Data Layer (Models & Schemas)               │
│ ├─ User, Machine, Permission, DigitalKey   │
│ └─ Pydantic Schemas for validation         │
├─────────────────────────────────────────────┤
│ Persistence Layer                           │
│ ├─ SQLite Database                         │
│ └─ Local Cloud Storage (JSON files)        │
└─────────────────────────────────────────────┘
```

## Security Features

- ✅ Digital key-based access control
- ✅ Role-based access control (RBAC)
- ✅ Permission levels enforcement
- ✅ Audit trails with timestamps
- ✅ Revocation tracking
- ✅ Foreign key constraints
- ✅ Unique constraints prevent duplicates

## Performance Considerations

- Automatic indexing on primary/foreign keys
- Pagination support on list endpoints
- Efficient query filtering
- Separate read/write endpoints
- Local caching potential

## Deployment

1. Install dependencies: `pip install -r requirements.txt`
2. Run migrations (auto-created by SQLAlchemy)
3. Start server: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
4. Verify health: `GET http://localhost:8000/`

## Future Enhancements

- JWT-based authentication
- Role-based authorization decorators
- Batch permission operations
- Time-based access windows
- Multi-factor authentication
- Geo-location restrictions
- Real-time access monitoring
- Advanced audit logging
- Permission expiration
- Access request workflow

## Contributing

Contributions are welcome! Please follow the existing code structure and patterns.

## Support

For issues, questions, or feature requests, please refer to the documentation files or create an issue in the repository.

## License

This project is licensed under the MIT License - see LICENSE file for details.

---

**Version**: 2.0  
**Last Updated**: January 19, 2026  
**Status**: Production Ready

### Get a Specific Digital Key

```bash
curl "http://localhost:8000/api/v1/digital-keys/1"
```

## Adding New Features

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

⚠️ **For production deployment**:

- Implement proper authentication and authorization (JWT recommended)
- Use environment variables for sensitive configuration
- Enable HTTPS/TLS
- Implement rate limiting
- Add input validation and sanitization
- Use proper error handling without exposing internal details
- Implement comprehensive logging and monitoring
- Configure CORS appropriately
- Use strong database backups
- Monitor local storage disk space

## Future Enhancements

- [ ] JWT-based authentication and authorization
- [ ] Advanced cloud storage integration (AWS S3, Azure Blob Storage)
- [ ] Key encryption and decryption
- [ ] Comprehensive audit logging
- [ ] API rate limiting
- [ ] Unit and integration tests
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Permission expiration
- [ ] Time-based access windows
- [ ] Batch operations
- [ ] Real-time monitoring

## Support

For issues, questions, or feature requests, please refer to the code documentation or create an issue in the repository.

## License

[Add your license here]

## Support

For issues and questions, please create an issue in the repository.