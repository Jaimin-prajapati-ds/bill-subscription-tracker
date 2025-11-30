# Bill Subscription Tracker

A powerful intermediate-level application for tracking recurring bills and subscriptions with real-time analytics, AI-powered insights, and intelligent renewal reminders.

## Problem Statement

Managing recurring payments across multiple services (OTT platforms, utilities, SaaS tools, insurance policies) is challenging:
- Multiple renewal dates across different platforms
- Forgotten subscriptions leading to wasted money
- No centralized expense tracking
- Difficulty identifying cost-saving opportunities
- Manual tracking prone to errors

Bill Subscription Tracker solves these issues with an integrated platform combining real-time tracking, smart analytics, and automation.

## Key Features

- **Full CRUD Operations**: Add, view, update, and delete subscriptions effortlessly
- **Smart Reminders**: Get alerts for subscriptions due today and in the next 7 days
- **Monthly Analytics**: Visualize spending by category with interactive Plotly charts
- **AI Insights**: Receive intelligent suggestions for optimizing subscription costs
- **Category Classification**: Organize subscriptions (OTT, Utility, Recharge, SaaS, Insurance, etc.)
- **CSV Export**: Download subscription data for external analysis or backup
- **Professional Dashboard**: Clean, intuitive Streamlit interface with real-time metrics

## Technology Stack

### Backend
- **FastAPI**: RESTful API with automatic OpenAPI documentation
- **SQLAlchemy**: ORM for relational database management
- **Pydantic**: Data validation and serialization

### Frontend
- **Streamlit**: Interactive web interface for rapid deployment
- **Plotly**: Interactive data visualization and analytics
- **Pandas**: Data manipulation and analysis

### Database
- **SQLite**: Lightweight, file-based relational database

### AI & Insights
- **OpenAI API**: Optional AI-powered suggestion engine

## Architecture

```
Client (Streamlit Frontend)
         |
         | HTTP/REST
         v
FastAPI Backend
    |
    | SQL
    v
SQLite Database
```

### Project Structure

```
bill-tracker/
  backend/
    main.py              # FastAPI application and endpoints
    models.py            # SQLAlchemy ORM models
    schemas.py           # Pydantic request/response schemas
    database.py          # Database engine and session setup
    crud.py              # Create, Read, Update, Delete operations
  frontend/
    app.py               # Streamlit web interface
  requirements.txt       # Python dependencies
  .env.example           # Environment configuration template
  README.md              # Documentation
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment tool

### Step 1: Clone Repository
```bash
git clone https://github.com/Jaimin-prajapati-ds/bill-subscription-tracker.git
cd bill-subscription-tracker
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings (optional: add OpenAI API key for AI features)
```

### Step 5: Run Backend
```bash
cd backend
uvicorn main:app --reload
# API will be available at http://localhost:8000
```

### Step 6: Run Frontend (In New Terminal)
```bash
cd frontend
streamlit run app.py
# Frontend will open at http://localhost:8501
```

## API Endpoints

### Subscriptions
- `POST /subscriptions` - Create new subscription
- `GET /subscriptions` - List all subscriptions
- `GET /subscriptions/{id}` - Get subscription details
- `PUT /subscriptions/{id}` - Update subscription
- `DELETE /subscriptions/{id}` - Delete subscription

### Analytics & Reminders
- `GET /subscriptions/due/today` - Get subscriptions due today
- `GET /subscriptions/due/soon?days=7` - Get subscriptions due within N days
- `GET /subscriptions/summary/monthly` - Get monthly spending summary by category
- `GET /insights/{id}` - Get AI-powered insights for a subscription

## Usage Guide

### Dashboard
View quick metrics: total subscriptions, monthly spending, renewals due.

### Add Subscription
Fill in subscription details:
- Name (e.g., Netflix, AWS, Electricity Bill)
- Amount (e.g., 499, 12000)
- Billing Cycle (monthly, annual, one-time)
- Next Due Date
- Category (OTT, Utility, SaaS, etc.)
- Optional notes

### Manage Subscriptions
View, update, or delete existing subscriptions with quick access to key details.

### Analytics
Interactive pie chart showing monthly spending breakdown by category. Identify which categories consume the most budget.

### Reminders
Automatically categorized notifications:
- Due Today (red warning)
- Due in Next 7 Days (yellow info)
- Color-coded for quick identification

### Export
Download all subscription data as CSV for spreadsheet analysis, backup, or data migration.

## Database Schema

```sql
CREATE TABLE subscriptions (
  id INTEGER PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  amount FLOAT NOT NULL,
  cycle VARCHAR(50) NOT NULL,  -- monthly, annual, one-time
  next_due DATE NOT NULL,
  category VARCHAR(100) NOT NULL,
  notes TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Performance Considerations

- Database indexed on `next_due` and `category` for fast filtering
- Stateless API design for horizontal scalability
- Streamlit caching for improved frontend performance
- Monthly cost calculations optimized with SQL aggregations

## Future Enhancements

- **User Authentication**: Multi-user support with secure login
- **Email Reminders**: Automated email notifications for due subscriptions
- **Budget Alerts**: Set spending limits per category with warnings
- **Multi-currency Support**: Handle international subscriptions
- **Recurring Task Automation**: Automatically update renewal dates
- **Advanced Analytics**: Spending trends, YoY comparisons, predictive analysis
- **Mobile App**: Native mobile application for on-the-go access
- **Integration APIs**: Connect with payment platforms and banks

## Testing

```bash
# Run API tests
cd tests
pytest test_api_subscriptions.py -v
```

## Deployment

### Streamlit Cloud
- Push code to GitHub
- Connect repository to Streamlit Cloud
- Frontend automatically deploys

### Backend (AWS, Heroku, DigitalOcean)
- Package as Docker container
- Deploy with uvicorn ASGI server
- Use managed PostgreSQL for production (replace SQLite)

## Security Best Practices

- Use environment variables for sensitive data (API keys)
- Validate all user inputs with Pydantic schemas
- Implement rate limiting for API endpoints
- Use HTTPS in production
- Regular dependency updates

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit changes with clear messages
4. Submit pull request with description

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Author

[Jaimin Prajapati](https://github.com/Jaimin-prajapati-ds)

If this project helped you, consider starring it on GitHub!

## Support

For issues, questions, or suggestions, please open a GitHub issue or contact the author.

---

**Track Smart. Pay Smart. Save More.**
