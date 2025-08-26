import pandas as pd
import joblib
import numpy as np
import os
from surprise import SVD
import time

# Nama file model
MODEL_FILE = 'system-recomendation.pkl'

# Variabel global untuk menyimpan model dan waktu modifikasi terakhir
model = None
last_modified_time = 0

def load_model():
    """
    Memuat model AI dari file .pkl hanya jika file telah diperbarui.
    Mengembalikan True jika model berhasil dimuat/sudah dimuat, False jika gagal.
    """
    global model, last_modified_time
    try:
        if not os.path.exists(MODEL_FILE):
            print(f"Error: File model '{MODEL_FILE}' tidak ditemukan.")
            model = None
            last_modified_time = 0
            return False
        
        current_mtime = os.path.getmtime(MODEL_FILE)

        # Periksa apakah model perlu dimuat ulang
        if model is None or current_mtime > last_modified_time:
            print(f"Perubahan terdeteksi. Memuat ulang model dari {MODEL_FILE}...")
            model = joblib.load(MODEL_FILE)
            last_modified_time = current_mtime
            print("Model berhasil dimuat.")
        else:
            print("Model sudah yang terbaru, tidak perlu memuat ulang.")
        
        return True
    except Exception as e:
        print(f"Error saat memuat model: {e}")
        model = None
        last_modified_time = 0
        return False

def get_recommendations(user_id, num_recommendations=5):
    """
    Menghasilkan rekomendasi produk untuk user_id tertentu.
    Akan memicu pemuatan ulang model jika diperlukan.
    """
    # Panggil load_model() untuk memeriksa apakah ada pembaruan pada file .pkl
    # Jika load_model() mengembalikan False, berarti ada masalah
    if not load_model():
        return {"error": "Gagal memuat model. Tidak dapat memberikan rekomendasi."}
    
    # ... (Sisa kode untuk menghasilkan rekomendasi tetap sama)
    # Gunakan objek 'model' global di sini
    try:
        df_training = pd.read_csv('data-training.csv')
        all_product_ids = df_training['product_id'].unique().tolist()
        
        predictions = []
        for product_id in all_product_ids:
            prediction = model.predict(user_id, int(product_id))
            predictions.append((int(product_id), prediction.est))
        
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        top_recommendations = predictions[:num_recommendations]
        
        recommendation_list = []
        for product_id, score in top_recommendations:
            recommendation_list.append({
                "product_id": int(product_id),
                "predicted_rating": float(f"{score:.2f}")
            })
            
        return {"recommendations": recommendation_list}

    except Exception as e:
        print(f"Error saat menghasilkan rekomendasi: {e}")
        return {"error": "Terjadi kesalahan internal saat menghasilkan rekomendasi."}