# News Curator - AI-Powered Personalized News Platform
**An AI-driven news aggregation and personalization platform built with Flask**  
Part of the #KremtAIDaysChallenge

[![Flask](https://img.shields.io/badge/Flask-2.3.2-blue)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Features
- **Role-Based Access Control**:
  - **Readers**: View personalized feeds, interact with content, comment
  - **Media Users**: Create and manage news articles
  - **Admins**: Manage users, roles, and content
  
- **AI-Powered Personalization**:
  - Content recommendations based on interaction history
  - Fallback to trending articles for new users
  - Category preference learning

- **Engagement Features**:
  - Article interactions (like/dislike/share/skip)
  - Commenting system with threaded discussions
  - Real-time interaction tracking

- **Content Management**:
  - Article creation with rich text editing
  - Role-based content deletion
  - Cascading deletion for removed users

- **User Experience**:
  - Responsive design with Tailwind CSS
  - Flash messaging for user feedback
  - Session-based authentication

## 🛠 Tech Stack
| Component              | Technology           |
|------------------------|----------------------|
| Backend Framework      | Python Flask         |
| Database               | SQLAlchemy + SQLite  |
| Frontend               | Tailwind CSS         |
| Authentication         | Flask-Login          |
| Forms                  | Flask-WTF            |
| Deployment             | Docker (optional)    |

## 🚀 Setup & Installation
### Prerequisites
- Python 3.9+
- Google Gemini API key

### Installation
```bash
# Clone repository
git clone https://github.com/Aman-byte1/ai-service-provider.git
cd ai-service-provider/news_curator

# Create virtual environment
python -m venv venv

# Activate environment (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
echo "SECRET_KEY='your_super_secret_key'" > .env
echo "GEMINI_API_KEY='your_api_key'" >> .env

# Initialize database
python init_db.py

# Run application
flask run
```

## 🧭 Usage
1. **Access the application**: `http://localhost:5000`
2. **Default admin credentials**: 
   - Username: `admin`
   - Password: `adminpassword`
3. **Key actions**:
   - Regular users: Browse feed, interact with articles
   - Media users: Create news via "Post News"
   - Admins: Manage users via "Manage Media"

## 📂 Project Structure
```
news_curator/
├── app.py                  # Main application
├── models.py               # Database models
├── forms.py                # WTForms definitions
├── routes/                 # Application routes
│   ├── auth.py             # Authentication
│   ├── main.py             # Core functionality
│   └── admin.py            # Admin controls
├── templates/              # Jinja templates
│   ├── base.html           # Base template
│   ├── auth/               # Auth templates
│   ├── news/               # News templates
│   └── admin/              # Admin templates
├── static/                 # Static assets
│   ├── css/                # Custom styles
│   └── js/                 # JavaScript files
└── requirements.txt        # Dependencies
```

## 🤝 Contributing
Contributions are welcome! Follow these steps:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a pull request

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.

## 📧 Contact
Aman-byte1 - [GitHub Profile](https://github.com/Aman-byte1)  
Project Link: [https://github.com/Aman-byte1/ai-service-provider](https://github.com/Aman-byte1/ai-service-provider)

---

**#KremtAIDaysChallenge** • **#Python** • **#Flask** • **#MachineLearning** • **#OpenSource**
```
