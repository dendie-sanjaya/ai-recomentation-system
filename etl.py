import pandas as pd
import sqlite3

def run_etl():
    """
    Extracts, transforms, and loads data from a SQL database into a CSV file,
    including user_id and product_id for recommendation mapping.
    """
    try:
        # 1. Extract: Hubungkan ke database dan ambil data
        conn = sqlite3.connect('my-database.db')
        
        # Perbaikan query: Tambahkan user_id dan product_id
        query = """
        SELECT
            p.user_id,
            pr.product_id,
            pr.rating,
            ph.visit_count,
            pre.review_text,
            pt.transaction_value,
            pp.category,
            pp.tag,
            pp.source_country
        FROM
            data_user_profile AS p
        LEFT JOIN
            data_product_rating AS pr ON p.user_id = pr.user_id
        LEFT JOIN
            data_user_history_visit_product AS ph ON p.user_id = ph.user_id
        LEFT JOIN
            data_product_reviews AS pre ON p.user_id = pre.user_id
        LEFT JOIN
            data_product_transaction_buy AS pt ON p.user_id = pt.user_id
        LEFT JOIN
            data_product_category_tag_source_country AS pp ON ph.product_id = pp.product_id;
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        print("Data extraction complete.")
        
        # 2. Transform: Bersihkan atau ubah data
        df.fillna(0, inplace=True) 
        
        # 3. Load: Simpan data ke file CSV
        output_file = 'data-training.csv'
        df.to_csv(output_file, index=False)
        
        print(f"Data successfully loaded to {output_file}.")
        
    except Exception as e:
        print(f"An error occurred during ETL process: {e}")

if __name__ == "__main__":
    run_etl()