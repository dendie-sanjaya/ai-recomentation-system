from flask import Flask, request, jsonify
import calculate
import get_info

app = Flask(__name__)

# Tidak perlu lagi memanggil calculate.load_model() di sini.
# Pemanggilan ini akan dilakukan di dalam fungsi get_recommendations().

@app.route('/recommend', methods=['GET'])
def recommend():
    """
    Endpoint API untuk mendapatkan rekomendasi produk yang diperkaya dengan detail.
    Menggunakan: /recommend?user_id=100
    """
    try:
        user_id = request.args.get('user_id', type=int)
        
        if user_id is None:
            return jsonify({"error": "Missing 'user_id' parameter."}), 400
        
        user_details = get_info.get_user_details(user_id)
        if not user_details:
            return jsonify({"error": "User not found in database."}), 404
            
        # Panggil fungsi get_recommendations.
        # Logika pemuatan ulang model ada di dalamnya.
        recommendations = calculate.get_recommendations(user_id)
        
        if "error" in recommendations:
            return jsonify(recommendations), 500
            
        product_ids_to_fetch = [rec['product_id'] for rec in recommendations['recommendations']]
        product_details = get_info.get_product_details(product_ids_to_fetch)
        
        final_recommendations_list = []
        for rec in recommendations['recommendations']:
            product_id = rec['product_id']
            full_product_data = {
                "product_id": product_id,
                "predicted_rating": rec['predicted_rating'],
                "details": product_details.get(product_id, {})
            }
            final_recommendations_list.append(full_product_data)
            
        response_data = {
            "user_id": user_id,
            "user_details": user_details,
            "recommendations": final_recommendations_list
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

if __name__ == '__main__':
    # Mulai aplikasi Flask
    app.run(host='0.0.0.0', port=5000, debug=True)