import pandas as pd
import joblib
from surprise import Reader, Dataset, SVD
from surprise.model_selection import train_test_split

def train_collaborative_model(data_file='data-training.csv', model_file='system-recomendation.pkl'):
    """
    Melatih model Collaborative Filtering (SVD) dan menyimpannya.
    """
    try:
        # 1. Memuat data dari file CSV
        print(f"Memuat data dari {data_file}...")
        df = pd.read_csv(data_file)
        
        # Pastikan data memiliki kolom yang dibutuhkan
        if not all(col in df.columns for col in ['user_id', 'product_id', 'rating']):
            print("Error: File CSV tidak memiliki kolom 'user_id', 'product_id', dan 'rating'.")
            return
        
        # 2. Persiapan data untuk library Surprise
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(df[['user_id', 'product_id', 'rating']], reader)
        
        # 3. Melatih model SVD
        print("Memulai pelatihan model Collaborative Filtering (SVD)...")
        trainset = data.build_full_trainset()
        algo = SVD(n_factors=100, n_epochs=20, lr_all=0.005, reg_all=0.02, random_state=42)
        algo.fit(trainset)
        
        print("Pelatihan model selesai.")
        
        # 4. Menyimpan model
        joblib.dump(algo, model_file)
        print(f"Model berhasil disimpan ke {model_file}.")
        
    except FileNotFoundError:
        print(f"Error: File '{data_file}' tidak ditemukan. Mohon pastikan file telah dibuat oleh proses ETL.")
    except Exception as e:
        print(f"Terjadi error selama pelatihan model: {e}")

if __name__ == "__main__":
    train_collaborative_model()