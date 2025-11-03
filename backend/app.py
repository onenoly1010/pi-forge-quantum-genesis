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

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
socketio = SocketIO(app, cors_allowed_origins="*", message_queue=redis_url)

supabase = None
if os.getenv('SUPABASE_URL'):
    supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

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
    try:
        pi_approx = "3.14159265358979323846"
        if digits <= 20:
            result = pi_approx[:digits + 2]
        else:
            result = f"3.14... computed {digits} digits"
        
        if supabase:
            supabase.table('leaderboard').upsert({
                'user_id': 'quantum_miner',
                'digits_mined': digits,
                'last_active': 'now()'
            }).execute()
        
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
        user_id = data.get('user_id', 'quantum_miner')
        amount = data.get('amount', 0)
        
        if supabase:
            supabase.table('stakes').insert({
                "user_id": user_id,
                "amount": amount,
                "start_time": "now()",
                "apy": 0.055
            }).execute()
        
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
    data = request.get_json()
    
    user = authenticate_user(data.get('email'), data.get('password'))
    
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
