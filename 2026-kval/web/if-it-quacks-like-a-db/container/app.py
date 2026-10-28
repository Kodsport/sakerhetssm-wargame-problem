from flask import Flask, render_template, request, jsonify
import duckdb
import pandas as pd
import os
from hashlib import md5

app = Flask(__name__)

# Flag stored in environment variable
FLAG = os.environ.get('FLAG', 'SSM{fake_flag_for_testing}')
FLAG_HINT = FLAG[:10]
FLAG2 = FLAG[10:]

# Initialize DuckDB connection. Start from a fresh file: it survives container
# restarts, and CREATE TABLE below fails if the tables already exist.
if os.path.exists('data.duckdb'):
    os.remove('data.duckdb')
conn = duckdb.connect('data.duckdb')

# Create products table with sample data
conn.execute("""
    CREATE TABLE products (
        id INTEGER,
        name VARCHAR,
        category VARCHAR,
        price DECIMAL(10,2),
        description VARCHAR
    );

    CREATE TABLE flags (
        id INTEGER,
        secret_type VARCHAR,
        secret_value VARCHAR
    );
""")

# Insert sample products
sample_products = [
    (1, 'Rubber Duck', 'Toys', 9.99, 'Classic yellow rubber duck for debugging'),
    (2, 'DuckDB Manual', 'Books', 29.99, 'Comprehensive guide to DuckDB'),
    (3, 'Duck Plushie', 'Toys', 14.99, 'Soft and cuddly duck plushie'),
    (4, 'Database for Dummies', 'Books', 24.99, 'Learn database basics'),
    (5, 'Duck Keychain', 'Accessories', 4.99, 'Cute duck keychain'),
    (6, 'SQL Injection Guide', 'Books', 39.99, 'Advanced SQL techniques'),
    (7, 'Flag Hint', 'Books', 19.99, 'Wow! Making so much progress: ' + FLAG_HINT),
]

for product in sample_products:
    conn.execute(f"""
        INSERT INTO products VALUES
        ({product[0]}, '{product[1]}', '{product[2]}', {product[3]}, '{product[4]}')
    """)

flag_data = pd.DataFrame({
    'id': [1],
    'secret_type': ['flag'],
    'secret_value': [FLAG2]
})

for flag in flag_data.itertuples():
    conn.execute(f"""
        INSERT INTO flags VALUES
        ({flag.id}, '{flag.secret_type}', '{md5(flag.secret_value.encode()).hexdigest()}')
    """)

conn.close()

ro_conn = duckdb.connect('data.duckdb', read_only=True)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    try:

        search_term = request.json.get('query', '')

        if not search_term:
            return jsonify({'error': 'No search query provided'}), 400

        # Format results
        columns = ['id', 'name', 'category', 'price', 'description']
        products = []


        # Execute the query
        result = ro_conn.execute(f"SELECT * FROM products WHERE description NOT LIKE '%{FLAG_HINT}%' AND name LIKE '%{search_term}%'").fetchall()

        for row in result:
            if not any(FLAG_HINT in str(cell) for cell in row):
                products.append(dict(zip(columns, row)))
            
        return jsonify({'products': products})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/check_flag', methods=['POST'])
def check_flag():
    try:
        submitted_flag = request.json.get('flag', '')

        if not submitted_flag:
            return jsonify({'error': 'No flag provided'}), 400
        
        if not submitted_flag.startswith(FLAG_HINT):
            return jsonify({'error': 'Flag does not start with hint'}), 400
        
        submitted_flag = submitted_flag[len(FLAG_HINT):] # check if the rest of the flag is correct

        query = f"SELECT * FROM flags WHERE secret_value = '{md5(submitted_flag.encode()).hexdigest()}'"

        print(f"Flag check query: {query}")

        try:
            result = ro_conn.execute(query).fetchall()

            if result:
                return jsonify({'correct': True, 'message': 'Flag is correct!'}), 200
            else:
                return jsonify({'correct': False, 'message': 'Flag is incorrect'}), 200

        except Exception as e:
            return jsonify({
                'error': e,
            }), 500

    except Exception as e:
        return jsonify({'error': 'Invalid request'}), 400

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'database': 'DuckDB', 'version': duckdb.__version__})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
