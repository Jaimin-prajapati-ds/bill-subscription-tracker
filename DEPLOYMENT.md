# Deployment Guide

## Production-Ready Bill Tracker

### Quick Start with Docker

```bash
# Clone repository
git clone https://github.com/Jaimin-prajapati-ds/bill-subscription-tracker
cd bill-subscription-tracker

# Create .env file
cp .env.example .env
# Edit .env with your settings

# Start with Docker Compose
docker-compose up --build
```

### Access the Application
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:8501

### Environment Variables

See `.env.example` for configuration options:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret for authentication
- `ENVIRONMENT`: development/production

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest -v

# With coverage
pytest --cov=backend
```

### Deployment to Render

1. Push to GitHub
2. Connect repository to Render
3. Set environment variables
4. Deploy

### Database Migrations

```bash
alembic upgrade head
```

### Production Checklist

- [ ] Change SECRET_KEY
- [ ] Use PostgreSQL (not SQLite)
- [ ] Enable HTTPS
- [ ] Setup database backups
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Review security headers
