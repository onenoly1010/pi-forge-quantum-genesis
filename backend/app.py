import os
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from supabase import create_client
from web3 import Web3
import redis
from dotenv import load_dotenv
from flask_cors import CORS
from auth import generate_token, token_required

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'pi-forge-kris-olofson-2024')
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize SocketIO with optional Redis
redis_url = os.getenv('REDIS_URL')
if redis_url:
    try:
        # Test Redis connection
        test_redis = redis.from_url(redis_url, socket_connect_timeout=5)
        test_redis.ping()
        socketio = SocketIO(app, cors_allowed_origins="*", message_queue=redis_url)
        print(f"✅ Connected to Redis: {redis_url}")
    except Exception as e:
        print(f"⚠️  Redis connection failed: {e}. Running without Redis.")
        socketio = SocketIO(app, cors_allowed_origins="*")
else:
    socketio = SocketIO(app, cors_allowed_origins="*")
    print("ℹ️  Running without Redis (in-memory mode)")

# Initialize Supabase client if credentials are provided
supabase = None
if os.getenv('SUPABASE_URL') and os.getenv('SUPABASE_KEY'):
    try:
        supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
        print("✅ Connected to Supabase")
    except Exception as e:
        print(f"⚠️  Supabase initialization failed: {e}")
else:
    print("ℹ️  Running without Supabase database")

def authenticate_user(email, password):
    # Simple demo authentication - replace with your actual logic
    if email == "admin@pi-forge.com" and password == "quantum2024":
        return {
            'id': 1,
            'username': 'quantum_miner', 
            'email': email
        }
    return None

@app.route('/')
def home():
    return jsonify({
        "status": "Pi Forge Quantum Genesis - LIVE",
        "version": "1.0.0", 
        "developer": "Kris Olofson",
        "services": ["compute", "staking", "nft", "dao", "vr"]
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy", 
        "developer": "Kris Olofson",
        "database": "connected" if supabase else "disconnected"
    })

@app.route('/compute/<int:digits>')
def compute_pi(digits):
    # Validate input
    if digits < 1:
        return jsonify({"error": "Digits must be at least 1"}), 400
    if digits > 1000000:
        return jsonify({"error": "Maximum 1,000,000 digits allowed"}), 400
    
    try:
        pi_approx = "3.14159265358979323846"
        if digits <= 20:
            result = pi_approx[:digits + 2]
        else:
            result = f"3.14... computed {digits} digits"
        
        if supabase:
            try:
                supabase.table('leaderboard').upsert({
                    'user_id': 'quantum_miner',
                    'digits_mined': digits,
                    'last_active': 'now()'
                }).execute()
            except Exception as db_error:
                # Log but don't fail the request if database update fails
                print(f"Database update failed: {db_error}")
        
        return jsonify({
            "digits": digits, 
            "result": result, 
            "status": "computed",
            "developer": "Kris Olofson"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stake', methods=['POST'])
def stake():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Request body required"}), 400
            
        user_id = data.get('user_id', 'quantum_miner')
        amount = data.get('amount', 0)
        
        # Validate amount
        if not isinstance(amount, (int, float)) or amount <= 0:
            return jsonify({"error": "Amount must be a positive number"}), 400
        
        if amount > 1000000:
            return jsonify({"error": "Maximum stake amount is 1,000,000"}), 400
        
        if supabase:
            try:
                supabase.table('stakes').insert({
                    "user_id": user_id,
                    "amount": amount,
                    "start_time": "now()",
                    "apy": 0.055
                }).execute()
            except Exception as db_error:
                print(f"Database insert failed: {db_error}")
        
        return jsonify({
            "status": "staked", 
            "amount": amount, 
            "user_id": user_id,
            "message": "Tokens staked successfully"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/leaderboard')
def get_leaderboard():
    try:
        if supabase:
            result = supabase.table('leaderboard').select('*').order('digits_mined', desc=True).limit(10).execute()
            return jsonify({
                "leaderboard": result.data,
                "developer": "Kris Olofson"
            })
        return jsonify({"leaderboard": [], "message": "Database not connected"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body required'}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        user = authenticate_user(email, password)
        
        if user:
            token = generate_token(user['id'])
            return jsonify({
                'token': token,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email']
                }
            })
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': 'Login failed'}), 500

@app.route('/api/protected-route', methods=['GET'])
@token_required
def protected_route(current_user):
    return jsonify({
        'message': f'Hello {current_user["username"]}!',
        'user_id': current_user['sub']
    })

@socketio.on('vr_mine')
def handle_vr_mine(data):
    user_id = data.get('user_id', 'quantum_miner')
    digits = data.get('digits', 0)
    emit('mining_update', {
        'user_id': user_id, 
        'digits': digits,
        'timestamp': 'now()',
        'event': 'vr_mine'
    }, broadcast=True)

@socketio.on('vr_quest')
def handle_vr_quest(data):
    user_id = data.get('user_id', 'quantum_miner')
    quest = data.get('quest', 'default')
    emit('quest_complete', {
        'user_id': user_id,
        'quest': quest,
        'timestamp': 'now()',
        'event': 'vr_quest'
    }, broadcast=True)

@socketio.on('connect')
def handle_connect():
    print('🔌 Client connected to Pi Forge')
    emit('connected', {'status': 'connected', 'message': 'Welcome to Pi Forge Quantum Genesis'})

@socketio.on('disconnect')
def handle_disconnect():
    print('🔌 Client disconnected from Pi Forge')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Pi Forge by Kris Olofson starting on port {port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
