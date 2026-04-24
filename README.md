# FinWise India - AI-Powered Financial Advisor

A comprehensive financial management web application designed specifically for middle-class users in India, providing personalized financial advice powered by AI.

## 🎯 Features

### Core Functionality
- **User Authentication**: Secure signup/login system
- **Financial Dashboard**: Overview of income, expenses, savings, and financial health
- **Expense Tracking**: Categorize and monitor daily expenses
- **Goal-Based Planning**: Set and track financial goals with progress visualization
- **AI Financial Advisor**: Personalized recommendations using OpenAI API
- **Budget Optimization**: Smart suggestions to reduce unnecessary spending
- **India-Specific Features**: INR currency, tax-saving options, inflation considerations

### Key Components
- **Smart Budgeting**: Categorize expenses (food, rent, travel, etc.)
- **Investment Guidance**: Recommendations for SIPs, mutual funds, FDs
- **Debt Management**: Track loans and suggest repayment strategies
- **Financial Forecasting**: Predict savings and wealth over time
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **AI Integration**: OpenAI API
- **Charts**: Chart.js for data visualization
- **Authentication**: Flask-Login with password hashing

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd finwise-india
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your API keys and secrets
   ```

5. **Initialize database**
   ```bash
   python app.py
   # The database will be created automatically
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 📁 Project Structure

```
finwise-india/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── finwise.db            # SQLite database (auto-created)
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Landing page
│   ├── login.html        # User login
│   ├── signup.html       # User registration
│   ├── dashboard.html    # Main dashboard
│   ├── add_expense.html  # Add expense form
│   ├── add_goal.html     # Add goal form
│   └── ai_advisor.html   # AI advisor interface
├── static/               # Static assets
│   ├── css/             # Custom CSS files
│   └── js/              # JavaScript files
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
SECRET_KEY=your-secret-key-change-this-in-production
OPENAI_API_KEY=your-openai-api-key-here
FLASK_ENV=development
```

### OpenAI API Setup

1. Sign up at [OpenAI Platform](https://platform.openai.com/)
2. Create an API key
3. Add the key to your `.env` file

## 📊 Database Schema

The application uses the following main models:

- **User**: User accounts with authentication
- **Expense**: Daily expense tracking with categories
- **Goal**: Financial goals with progress tracking
- **Debt**: Loan and debt management
- **Investment**: Investment portfolio tracking

## 🇮🇳 India-Specific Features

- **Currency**: Full INR support with proper formatting
- **Categories**: Expense categories relevant to Indian households
- **Tax Options**: Consideration for ELSS, PPF, and other tax-saving instruments
- **Inflation**: Built-in inflation calculations for long-term planning
- **Family Support**: Categories for joint family expenses

## 🤖 AI Advisor Features

The AI advisor provides:

- **Budget Optimization**: Identify areas to reduce spending
- **Savings Recommendations**: Personalized savings strategies
- **Investment Advice**: Suitable for Indian markets and risk profiles
- **Debt Repayment**: Prioritization strategies for loans
- **Goal Planning**: Roadmaps to achieve financial objectives

## 🔒 Security Features

- Password hashing with bcrypt
- Session-based authentication
- CSRF protection
- Input validation and sanitization
- Secure data handling

## 📱 Responsive Design

- Mobile-first approach
- Touch-friendly interface
- Adaptive layouts for all screen sizes
- Modern UI with Tailwind CSS

## 🚀 Deployment

For production deployment:

1. Set `FLASK_ENV=production`
2. Use a production WSGI server (Gunicorn)
3. Configure a proper database (PostgreSQL/MySQL)
4. Set up SSL/TLS certificates
5. Use environment variables for sensitive data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:

1. Check the existing issues
2. Create a new issue with detailed description
3. Include error logs and screenshots if applicable

## 🌟 Future Enhancements

- [ ] Mobile app development
- [ ] Advanced analytics and reporting
- [ ] Integration with Indian banking APIs
- [ ] Mutual fund recommendations
- [ ] Tax planning tools
- [ ] Retirement planning calculator
- [ ] Insurance recommendations

---

**FinWise India** - Your trusted partner in financial wellness! 💰✨
