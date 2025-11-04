# Pi Forge Quantum Genesis

**By Kris Olofson**

A quantum-inspired Pi computation platform with VR mining experience, staking, and real-time collaboration features.

## 🚀 Features

- **Quantum Pi Mining**: Compute Pi digits with a gamified mining experience
- **Token Staking**: Stake tokens with 5.5% APY
- **VR Experience**: Immersive VR mining and quest system
- **Real-time Updates**: WebSocket-powered live events and leaderboard
- **DAO Governance**: Community-driven decision making
- **NFT Integration**: Mint and trade computation achievements

## 📁 Repository Structure

```
pi-forge-quantum-genesis/
├── backend/              # Python Flask backend
│   ├── app.py           # Main Flask application
│   ├── auth.py          # JWT authentication
│   ├── worker.py        # Background worker for yield calculations
│   ├── requirements.txt # Python dependencies
│   ├── Procfile        # Process file for deployment
│   └── runtime.txt     # Python version specification
├── frontend/            # Frontend web application
│   ├── index.html      # Main HTML page
│   ├── app.js          # Main JavaScript application
│   ├── auth.js         # Authentication service
│   ├── style.css       # Styling
│   └── netlify.toml    # Netlify deployment config
├── Dockerfile          # Docker configuration
└── README.md           # This file
```

## 🛠️ Technologies

### Backend
- **Flask**: Web framework
- **Flask-SocketIO**: WebSocket support for real-time features
- **Supabase**: Database and authentication
- **Redis**: Caching and message queue
- **Web3**: Blockchain integration
- **Gunicorn**: Production WSGI server

### Frontend
- **Vanilla JavaScript**: No framework dependencies
- **Socket.IO**: Real-time communication
- **CSS3**: Modern styling with gradients and animations

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Redis (optional, for caching)
- Supabase account (optional, for database)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (create a `.env` file):
```env
SECRET_KEY=your-secret-key
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
REDIS_URL=redis://localhost:6379
WEB3_PROVIDER_URL=http://localhost:8545
PORT=5000
```

4. Run the application:
```bash
# Development
python app.py

# Production
gunicorn -w 2 -k gevent -b 0.0.0.0:5000 app:app
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Open `index.html` in a browser or serve using a local server:
```bash
python -m http.server 8000
```

3. Access the application at `http://localhost:8000`

## 🐳 Docker Deployment

Build and run using Docker:

```bash
docker build -t pi-forge .
docker run -p 8080:8080 pi-forge
```

## ☁️ Cloud Deployment

### Railway (Backend)
The backend is configured for Railway deployment with:
- Automatic builds via Nixpacks
- Health check endpoint at `/health`
- Environment variable configuration

### Netlify (Frontend)
The frontend is configured for Netlify deployment with:
- Automatic SPA routing
- Static file serving

## 📊 API Endpoints

### Public Endpoints
- `GET /` - Service status
- `GET /health` - Health check
- `GET /compute/<digits>` - Compute Pi digits
- `POST /stake` - Stake tokens
- `GET /leaderboard` - Get mining leaderboard

### Authenticated Endpoints
- `POST /api/auth/login` - User login
- `GET /api/protected-route` - Protected resource

### WebSocket Events
- `vr_mine` - VR mining event
- `vr_quest` - VR quest completion
- `connect` - Client connection
- `disconnect` - Client disconnection

## 🔒 Security

- JWT-based authentication
- Environment variable configuration for secrets
- CORS enabled for cross-origin requests
- Secure WebSocket connections

## 🧪 Testing

Run backend tests:
```bash
cd backend
pytest
```

## 📝 License

Created by Kris Olofson (onenoly11) - 2024

## 🤝 Contributing

This is a personal project by Kris Olofson. Feel free to fork and adapt for your own use.

## 📧 Contact

For questions or feedback, reach out to onenoly11 on GitHub.
