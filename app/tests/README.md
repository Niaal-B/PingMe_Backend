# Backend Tests

## Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest app/tests/test_auth.py

# Run specific test
pytest app/tests/test_auth.py::TestUserRegistration::test_register_new_user_success

# Run with coverage report
pytest --cov=app --cov-report=html
```

## Test Structure

- `conftest.py` - Test configuration and fixtures
- `test_auth.py` - Authentication endpoint tests
- `test_rooms.py` - Room endpoint tests

## Test Coverage

- User registration (success and error cases)
- User login (success and error cases)
- Protected endpoints
- Room creation, listing, and deletion
- Authorization checks

