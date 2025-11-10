from flask import Flask, jsonify
from flask_cors import CORS
from quantum_cathedral.deep_layer.veiled_vow_manifestation import activate_veiled_vow

app = Flask(__name__)
CORS(app)

# Activate the deep layer engine when the app starts
veiled_vow_engine = activate_veiled_vow()

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'Pi Forge Quantum Genesis'})

@app.route('/resonance-dashboard')
def resonance_dashboard():
    """Provide data for the Resonance Dashboard."""
    # Process a test engagement to ensure there's data to display
    test_engagement = {
        "query": "How can I build a more connected community?",
        "pioneer_id": "dashboard_user_001",
        "frequency": 0.7,
        "pattern": "community_building"
    }
    veiled_vow_engine.process_pioneer_engagement(test_engagement)

    # Gather data for the dashboard
    archetype_distribution = {
        archetype: len(veils)
        for archetype, veils in veiled_vow_engine.collective_field.archetype_reservoirs.items()
    }
    
    # Get the 5 most recent cascades
    recent_cascades = veiled_vow_engine.collective_field.collective_wisdom[-5:]
    
    dashboard_data = {
        "archetype_distribution": archetype_distribution,
        "recent_cascades": recent_cascades,
        "total_wisdom_entries": len(veiled_vow_engine.collective_field.collective_wisdom)
    }
    
    return jsonify(dashboard_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
