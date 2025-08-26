import sqlite3
import pandas as pd

# Nama file database SQLite
DATABASE_FILE = 'my-database.db' # Sesuai dengan nama file yang Anda berikan

def get_db_connection():
    """
    Membuat dan mengembalikan koneksi ke database SQLite.
    """
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        return conn
    except sqlite3.Error as e:
        print(f"Error: Gagal terhubung ke database. {e}")
        return None

def get_user_details(user_id):
    """
    Mengambil detail pengguna dari tabel data_user_profile.
    Sekarang termasuk kolom 'name'.
    """
    conn = get_db_connection()
    if conn is None:
        return None

    try:
        query = "SELECT name, gender, age, location FROM data_user_profile WHERE user_id = ?"
        user_details = pd.read_sql_query(query, conn, params=(user_id,)).to_dict('records')
        
        if user_details:
            return user_details[0]
        else:
            return None
    except pd.io.sql.DatabaseError as e:
        print(f"Error saat mengambil detail pengguna: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_product_details(product_ids):
    """
    Mengambil detail produk dari tabel data_product_category_tag_source_country.
    Sekarang menyertakan nama, kategori, tag, dan negara asal.
    """
    conn = get_db_connection()
    if conn is None:
        return {}
    
    # Mengonversi list product_ids menjadi string yang bisa digunakan dalam klausa IN
    placeholders = ','.join('?' * len(product_ids))
    
    try:
        # Mengambil informasi produk yang lebih detail sesuai dengan skema Anda
        query = f"SELECT product_id, product_name, category, tag, source_country FROM data_product_category_tag_source_country WHERE product_id IN ({placeholders})"
        product_details = pd.read_sql_query(query, conn, params=product_ids).to_dict('records')
        
        # Mengubah format list of dictionaries menjadi dictionary dengan product_id sebagai key
        return {item['product_id']: item for item in product_details}
    except pd.io.sql.DatabaseError as e:
        print(f"Error saat mengambil detail produk: {e}")
        return {}
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # --- Contoh Penggunaan ---
    
    # Contoh detail pengguna
    user_id_test = 1
    details = get_user_details(user_id_test)
    print(f"Detail Pengguna {user_id_test}: {details}")

    # Contoh detail produk
    product_ids_test = [1, 2, 3]
    prod_details = get_product_details(product_ids_test)
    print(f"\nDetail Produk untuk ID {product_ids_test}: {prod_details}")