# API-key-generator
Secure Flask middleware for RestCountries API with user authentication, API key management, and streamlined country data retrieval. Features bcrypt password hashing, session management, and SQLite database.


# Countries Information API Middleware

A secure Flask-based API middleware service that interfaces with RestCountries.com to provide streamlined country information with robust authentication and API key management.

## Overview

This application serves as an intelligent intermediary layer between clients and the RestCountries.com API, implementing comprehensive security measures while delivering essential country data in a simplified format.

## Features

### Core Functionality
- **Country Data Retrieval**: Fetch detailed information about any country including:
  - Common and official names
  - Capital city
  - Currencies (code, name, symbol)
  - Spoken languages
  - National flag

### Security & Authentication
- User registration with input validation
- Secure login system with bcrypt password hashing
- Session-based authentication
- API key generation and management
- Key activation/deactivation controls
- Request tracking with usage timestamps

### User Dashboard
- Clean, modern interface built with Tailwind CSS
- API key display with copy-to-clipboard functionality
- Real-time key status monitoring (enabled/disabled)
- Usage statistics (creation date, last used)
- One-click key toggle functionality

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite3
- **Authentication**: Flask-Bcrypt for password hashing
- **Frontend**: HTML, Tailwind CSS
- **External API**: RestCountries.com v3.1

## Project Structure

```
├── auth.py              # Authentication routes (register, login, logout)
├── apiKey.py            # API key generation and management
├── countriesInfo.py     # Country data retrieval endpoints
├── Database/
│   └── database.py      # Database initialization and connection
├── Users/
│   └── bcrypt_extension.py  # Password hashing utilities
└── templates/
    ├── index.html       # Login page
    ├── signup.html      # Registration page
    └── dashboard.html   # User dashboard
```

## Database Schema

### Users Table
```sql
- id (PRIMARY KEY)
- username (UNIQUE)
- email (UNIQUE)
- password (hashed)
```

### API Keys Table
```sql
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- api_key
- is_active (BOOLEAN)
- created_at (TIMESTAMP)
- last_used (TIMESTAMP)
```

### API Usage Table
```sql
- id (PRIMARY KEY)
- api_key_id (FOREIGN KEY)
- endpoint
- timestamp
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/countries-api-middleware.git
cd countries-api-middleware
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install flask flask-bcrypt requests
```

4. Initialize the database:
```bash
python -c "from Database.database import init_db; init_db()"
```

5. Run the application:
```bash
flask run
```

## API Usage

### Authentication
All API requests require a valid API key passed in the request headers:

```bash
X-API-KEY: your_api_key_here
```

### Endpoints

#### Get Country Information
```bash
GET /country/<country_name>
```

**Example Request:**
```bash
curl -H "X-API-KEY: your_api_key" http://localhost:5000/country/france
```

**Example Response:**
```json
{
  "name": "France",
  "official_name": "French Republic",
  "capital": "Paris",
  "currencies": [
    {
      "code": "EUR",
      "name": "Euro",
      "symbol": "€"
    }
  ],
  "languages": ["French"],
  "flag": "https://flagcdn.com/w320/fr.png"
}
```

## Security Features

- **Password Hashing**: All passwords are hashed using bcrypt before storage
- **Session Management**: Secure session-based authentication
- **API Key Validation**: Keys are validated on every request
- **Active Key Tracking**: Inactive keys are automatically rejected
- **Usage Monitoring**: Last-used timestamps for all API keys

## Validation Rules

### Registration
- Username: Minimum 3 characters
- Password: Minimum 6 characters
- Email: Valid email format required

### API Keys
- Format: 10 characters (alphanumeric)
- Must contain: At least 1 uppercase, 1 lowercase, 3 digits
- One active key per user

## Docker Support (Recommended for Deployment)

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install flask flask-bcrypt requests
CMD ["flask", "run", "--host=0.0.0.0"]
```

Build and run:
```bash
docker build -t countries-api .
docker run -p 5000:5000 countries-api
```

## Future Enhancements

- Rate limiting per API key
- Advanced analytics dashboard
- Multiple API key support per user
- Webhook notifications
- API documentation with Swagger/OpenAPI

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [RestCountries.com](https://restcountries.com) for providing the country data API
- Flask community for excellent documentation and support

## Contact

For questions or feedback, please open an issue on GitHub.
