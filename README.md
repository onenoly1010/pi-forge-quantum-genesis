# 🧠 Pi Forge Quantum Genesis

**By Kris Olofson (onenoly1010)**

A revolutionary quantum-inspired Pi computation platform with blockchain integration, real-time staking, VR mining experiences, and WebSocket-powered live updates.

## 🌟 Features

- **⚡ Quantum Pi Mining**: Compute Pi digits using quantum-inspired algorithms
- **💰 Token Staking**: Stake tokens with 5.5% APY
- **🎮 VR Mining Experience**: Immersive virtual reality mining sessions
- **🏆 Live Leaderboard**: Real-time competition tracking
- **🔐 JWT Authentication**: Secure user authentication
- **🔔 WebSocket Events**: Real-time updates via Socket.IO
- **🌐 Web3 Integration**: Blockchain-ready architecture
- **📊 Supabase Database**: Scalable cloud database integration

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- pip
- Redis (optional, for production)
- Supabase account (optional, for database features)

### Installation

```bash
# Clone the repository
git clone https://github.com/onenoly1010/pi-forge-quantum-genesis.git
cd pi-forge-quantum-genesis

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Run the application
python app.py
```

The application will start on `http://localhost:5000`

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
SECRET_KEY=your-secret-key
PORT=5000
REDIS_URL=redis://localhost:6379
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
```

## 📚 API Endpoints

### Public Endpoints

- `GET /` - Service status and information
- `GET /health` - Health check endpoint
- `GET /compute/<digits>` - Compute Pi to specified digits
- `POST /stake` - Stake tokens
- `GET /leaderboard` - Get mining leaderboard

### Authentication Endpoints

- `POST /api/auth/login` - User login (returns JWT token)
- `GET /api/protected-route` - Protected route example (requires authentication)

### WebSocket Events

- `connect` - Client connection established
- `vr_mine` - VR mining session event
- `vr_quest` - VR quest completion event
- `disconnect` - Client disconnection

## 🏗️ Architecture

```
pi-forge-quantum-genesis/
├── backend/              # Flask backend application
│   ├── app.py           # Main Flask app with API endpoints
│   ├── auth.py          # JWT authentication logic
│   ├── worker.py        # Background worker tasks
│   └── requirements.txt # Python dependencies
├── frontend/            # Frontend web interface
│   ├── index.html       # Main UI
│   ├── app.js          # Frontend logic
│   ├── auth.js         # Authentication handling
│   └── style.css       # Styling
├── Dockerfile          # Container configuration
└── nixpacks.toml       # Deployment configuration
```

## 🔧 Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run verification script
python verify.py
```

### Running with Docker

```bash
# Build the image
docker build -t pi-forge .

# Run the container
docker run -p 8080:8080 pi-forge
```

## 🌐 Deployment

This application is deployment-ready for platforms like:
- Railway
- Heroku
- AWS
- Google Cloud Platform
- Azure

Configuration files included:
- `Dockerfile` for containerized deployment
- `nixpacks.toml` for Nixpacks-based platforms
- `railway.json` for Railway deployment

## 📖 Documentation

For detailed installation and setup instructions, see [INSTALL.md](INSTALL.md)

## 🛡️ Security

- JWT-based authentication with configurable expiration
- Secure secret key management via environment variables
- CORS protection with configurable origins
- Token validation on protected routes

## 🤝 Contributing

This is a personal project by Kris Olofson. For questions or collaboration inquiries, please open an issue.

## 📄 License

Copyright © 2024 Kris Olofson. All rights reserved.

## 🎯 Roadmap

- [ ] Enhanced quantum algorithms
- [ ] NFT marketplace integration
- [ ] DAO governance features
- [ ] Advanced VR experiences
- [ ] Mobile app development

---

**Built with Quantum Spirit by Kris Olofson | Pi Forge Genesis 2024** 🔬
