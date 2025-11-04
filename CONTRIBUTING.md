# Contributing to Pi Forge Quantum Genesis

Thank you for your interest in contributing to Pi Forge Quantum Genesis!

## Development Setup

### Backend Development

1. Set up a Python virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file based on `.env.example`

4. Run the development server:
```bash
python app.py
```

### Frontend Development

The frontend uses vanilla JavaScript with no build step required.

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Start a local development server:
```bash
python -m http.server 8000
```

3. Open `http://localhost:8000` in your browser

## Code Style

### Python
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose

### JavaScript
- Use ES6+ features (const, let, arrow functions, etc.)
- Use camelCase for variables and functions
- Add comments for complex logic
- Keep functions pure when possible

### General
- Write clear commit messages
- Test your changes before committing
- Update documentation when adding features

## Project Structure

```
pi-forge-quantum-genesis/
├── backend/              # Python Flask backend
│   ├── app.py           # Main application
│   ├── auth.py          # Authentication logic
│   └── worker.py        # Background worker
├── frontend/            # Frontend application
│   ├── index.html      # Main page
│   ├── app.js          # Application logic
│   ├── auth.js         # Authentication service
│   └── style.css       # Styling
└── docs/               # Documentation
```

## Testing

Before submitting changes:

1. Test backend endpoints manually or with automated tests
2. Verify frontend functionality in multiple browsers
3. Check for console errors
4. Ensure responsive design works on mobile

## Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Questions?

Feel free to open an issue for any questions or suggestions!
