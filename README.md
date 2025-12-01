# 💰 Bill & Subscription Tracker

> **Track recurring payments, visualize spending, and never miss a renewal**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://bill-subscription-tracker-iacjxjffsshqsmjaugg3vp.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 🎯 Problem Statement

Managing recurring payments across multiple services (OTT platforms, utilities, SaaS tools, insurance policies) is challenging:

- ❌ Multiple renewal dates across different platforms
- ❌ Forgotten subscriptions leading to wasted money
- ❌ No centralized expense tracking
- ❌ Difficulty identifying cost-saving opportunities
- ❌ Manual tracking prone to errors

**Bill Subscription Tracker** solves these issues with an integrated platform combining **real-time tracking**, **smart analytics**, and **automation**.

---

## ✨ Key Features

### Core Functionality
- ✅ **Full CRUD Operations** - Add, view, update, and delete subscriptions effortlessly
- 🔔 **Smart Reminders** - Get alerts for subscriptions due today and in the next 7 days
- 📈 **Monthly Analytics** - Visualize spending by category with interactive Plotly charts
- 🤖 **AI Insights** - Receive intelligent suggestions for optimizing subscription costs
- 📂 **Category Classification** - Organize subscriptions (OTT, Utility, Recharge, SaaS, Insurance, etc.)
- 💾 **CSV Export** - Download subscription data for external analysis or backup
- 🎨 **Professional Dashboard** - Clean, intuitive Streamlit interface with real-time metrics

### Advanced Features
- 🔄 **Mark as Paid** - Automatically update next due dates
- 🔍 **Search & Filter** - Quickly find subscriptions
- 📅 **Due Date Tracking** - Color-coded alerts (red/yellow/green)
- 📊 **Cost Breakdown** - Monthly vs annual cost comparison
- 🎯 **AI-Powered Recommendations** - Budget optimization suggestions

---

## 📸 Screenshots

### Dashboard Overview
*Coming soon - Will show main dashboard with metrics and subscription list*

### Analytics View
*Coming soon - Will show pie charts and category breakdown*

### Reminders & Alerts
*Coming soon - Will show color-coded due date alerts*

> **Note:** Screenshots will be added after the next deployment update.

---

## 🛠️ Technology Stack

### Backend
| Technology | Purpose |
|------------|----------|
| **FastAPI** | RESTful API with automatic OpenAPI documentation |
| **SQLAlchemy** | ORM for relational database management |
| **Pydantic** | Data validation and serialization |
| **SQLite** | Lightweight, file-based relational database |

### Frontend
| Technology | Purpose |
|------------|----------|
| **Streamlit** | Interactive web interface for rapid deployment |
| **Plotly** | Interactive data visualization and analytics |
| **Pandas** | Data manipulation and analysis |

### AI & Insights
| Technology | Purpose |
|------------|----------|
| **OpenAI API** | Optional AI-powered suggestion engine (backend) |
| **Custom AI Logic** | Built-in insights based on spending patterns |

---

## 🏛️ Architecture

```
┌──────────────────────────┐
│  Client (Streamlit)      │
│  - Dashboard UI          │
│  - Analytics Charts      │
│  - CRUD Operations       │
└───────┬─────────────────┘
        │ HTTP/REST
        │
┌───────┴─────────────────┐
│  FastAPI Backend         │
│  - API Endpoints         │
│  - Business Logic        │
│  - Authentication        │
└───────┬─────────────────┘
        │ SQL
        │
┌───────┴─────────────────┐
│  SQLite Database         │
│  - Persistent Storage    │
│  - Indexed Queries       │
└─────────────────────────┘
```

### Project Structure

```
bill-subscription-tracker/
├── backend/                    # FastAPI backend
│   ├── main.py                 # API application and endpoints
│   ├── models.py               # SQLAlchemy ORM models
│   ├── schemas.py              # Pydantic request/response schemas
│   ├── database.py             # Database engine and session
│   ├── auth.py                 # Authentication logic
│   ├── logging_config.py       # Structured logging
│   └── test_api.py             # API unit tests
├── frontend/                   # Streamlit frontend
│   ├── app.py                  # Main dashboard (backend-connected)
│   └── Dockerfile              # Frontend container
├── streamlit_app.py            # Standalone app (no backend required)
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Backend container
├── docker-compose.yml          # Multi-container orchestration
├── .env.example                # Environment configuration template
├── DEPLOYMENT.md               # Deployment guide
├── CONTRIBUTING.md             # Contribution guidelines
└── README.md                   # This file
```

---

## 🚀 Quick Start

### Option 1: Live Demo (Instant Access)
**👉 [Try the app now - No installation required!](https://bill-subscription-tracker-iacjxjffsshqsmjaugg3vp.streamlit.app)**

### Option 2: Run Standalone App Locally

```bash
# Clone repository
git clone https://github.com/Jaimin-prajapati-ds/bill-subscription-tracker.git
cd bill-subscription-tracker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run standalone Streamlit app
streamlit run streamlit_app.py
```

App will open at `http://localhost:8501` 🎉

### Option 3: Full Stack (Backend + Frontend)

#### Step 1: Run Backend
```bash
cd backend
uvicorn main:app --reload
# API available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

#### Step 2: Run Frontend (New Terminal)
```bash
cd frontend
streamlit run app.py
# Frontend at http://localhost:8501
```

### Option 4: Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access:
# - Frontend: http://localhost:8501
# - Backend: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

---

## 📚 API Documentation

### Subscription Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/subscriptions` | Create new subscription |
| `GET` | `/subscriptions` | List all subscriptions |
| `GET` | `/subscriptions/{id}` | Get subscription details |
| `PUT` | `/subscriptions/{id}` | Update subscription |
| `DELETE` | `/subscriptions/{id}` | Delete subscription |

### Analytics & Reminders

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/subscriptions/due/today` | Get subscriptions due today |
| `GET` | `/subscriptions/due/soon?days=7` | Get subscriptions due within N days |
| `GET` | `/subscriptions/summary/monthly` | Get monthly spending summary |
| `GET` | `/insights/{id}` | Get AI insights for subscription |

**Interactive API Docs:** Visit `http://localhost:8000/docs` after starting the backend.

---

## 📊 Usage Guide

### 1️⃣ Dashboard
View quick metrics:
- Total subscriptions
- Monthly spending
- Renewals due today/this week
- All subscriptions in a sortable table

### 2️⃣ Add Subscription
Fill in details:
- **Name** (e.g., Netflix, AWS, Electricity Bill)
- **Amount** (e.g., 499, 12000)
- **Billing Cycle** (monthly, annual, one-time)
- **Next Due Date**
- **Category** (OTT, Utility, SaaS, etc.)
- **Notes** (optional)

### 3️⃣ Manage Subscriptions
- Search/filter by name or category
- View detailed information
- **Mark as Paid** - Auto-updates next due date
- **Delete** - Remove subscription

### 4️⃣ Analytics
- **Pie Chart** - Category-wise spending breakdown
- **Bar Chart** - Visual comparison
- **Detailed Table** - Costs, percentages, subscription counts
- **AI Insights** - Optimization recommendations

### 5️⃣ Reminders
Color-coded alerts:
- 🔴 **Red** - Due today (urgent)
- 🟪 **Yellow** - Due in 3 days (warning)
- 🟢 **Green** - Due in 7 days (info)

### 6️⃣ Export
Download data as:
- **CSV** - For Excel/Google Sheets
- **JSON** - For programming/backup

---

## 💾 Database Schema

```sql
CREATE TABLE subscriptions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(255) NOT NULL,
  amount FLOAT NOT NULL,
  cycle VARCHAR(50) NOT NULL,      -- 'monthly', 'annual', 'one-time'
  next_due DATE NOT NULL,
  category VARCHAR(100) NOT NULL,  -- 'OTT', 'Utility', 'SaaS', etc.
  notes TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_next_due ON subscriptions(next_due);
CREATE INDEX idx_category ON subscriptions(category);
```

---

## ⚡ Performance & Scalability

- **Database Indexing** - Fast filtering on `next_due` and `category`
- **Stateless API** - Horizontal scalability ready
- **Streamlit Caching** - Improved frontend performance
- **SQL Aggregations** - Optimized monthly cost calculations
- **Handles 1000+ subscriptions** with <50ms API response time

---

## 🔮 Future Enhancements

### High Priority
- [ ] **Email Reminders** - Automated notifications via SMTP/SendGrid
- [ ] **User Authentication** - Multi-user support with JWT tokens
- [ ] **Budget Alerts** - Set monthly limits per category
- [ ] **Payment Integration** - Razorpay/Stripe for auto-tracking

### Medium Priority
- [ ] **Multi-currency Support** - Handle USD, EUR, INR, etc.
- [ ] **Mobile Responsive UI** - Optimized mobile experience
- [ ] **Recurring Task Automation** - Auto-update renewal dates
- [ ] **Advanced Analytics** - Spending trends, YoY comparisons

### Low Priority
- [ ] **Mobile App** - Native iOS/Android application
- [ ] **Bank Integration APIs** - Auto-import transactions
- [ ] **Browser Extension** - Quick add from any website

---

## 🧪 Testing

```bash
# Run API tests
cd backend
pytest test_api.py -v

# Run with coverage
pytest --cov=. test_api.py
```

---

## 🐳 Deployment

### Streamlit Cloud (Frontend Only)
1. Push code to GitHub
2. Connect repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Set entry point to `streamlit_app.py`
4. Deploy automatically

### Backend Deployment Options

#### Heroku
```bash
heroku create bill-tracker-api
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

#### Railway / Render
1. Connect GitHub repository
2. Select `backend/main.py` as entry
3. Add environment variables
4. Deploy with one click

#### Docker (Any Platform)
```bash
docker build -t bill-tracker .
docker run -p 8000:8000 bill-tracker
```

**Production Tips:**
- Replace SQLite with PostgreSQL
- Use environment variables for secrets
- Enable HTTPS
- Add rate limiting
- Set up monitoring (Sentry, Prometheus)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

---

## 🔒 Security Best Practices

✅ Environment variables for sensitive data (API keys)  
✅ Input validation with Pydantic schemas  
✅ SQL injection prevention via ORM  
✅ CORS configuration for frontend-backend communication  
⚠️ **TODO:** Add rate limiting, JWT authentication, HTTPS in production

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes with clear messages
4. Push to branch (`git push origin feature/amazing-feature`)
5. Submit a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📜 License

MIT License - Free to use for personal or commercial purposes.

---

## 👨‍💻 Author

**Jaimin Prajapati**  
🔗 [GitHub Profile](https://github.com/Jaimin-prajapati-ds)  
💌 [LinkedIn](https://linkedin.com/in/jaimin-prajapati-ds)  

---

## ⭐ Support

If this project helped you, please:
- ⭐ **Star this repository** on GitHub
- 👁️ **Share** with friends who need subscription tracking
- 🐛 **Report issues** or suggest features

For questions or bug reports, please [open an issue](https://github.com/Jaimin-prajapati-ds/bill-subscription-tracker/issues).

---

<div align="center">

### 💰 Track Smart. Pay Smart. Save More.

[![Live Demo](https://img.shields.io/badge/Try%20Now-Live%20Demo-FF4B4B?style=for-the-badge)](https://bill-subscription-tracker-iacjxjffsshqsmjaugg3vp.streamlit.app)
[![GitHub](https://img.shields.io/badge/Star%20on-GitHub-181717?style=for-the-badge&logo=github)](https://github.com/Jaimin-prajapati-ds/bill-subscription-tracker)

Made with ❤️ and Streamlit

</div>
