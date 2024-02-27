from flask import Flask, request, jsonify, make_response
import psycopg2
from flask_bcrypt import Bcrypt
from jwt import encode

app = Flask(__name__)
bcrypt = Bcrypt(app)

SERVER_ADDRESS = "localhost"
SERVER_PORT = 8080

try:
    conn = psycopg2.connect(dsn="$POSTGRES_CONN")
except psycopg2.Error as error:
    print(f"PostgreSQL connection error: {error}")
    exit(1)

#task1
@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok"}), 200

#task2.1
@app.route('/api/countries', methods=['GET'])
def get_countries():
    cur = conn.cursor()
    cur.execute("SELECT * FROM countries")
    countries = cur.fetchall()
    return jsonify(countries), 200

#task2.2
@app.route('/api/countries/<alpha2>', methods=['GET'])
def get_country_by_alpha2(alpha2):
    cur = conn.cursor()
    cur.execute("SELECT * FROM countries WHERE alpha2 = %s", (alpha2,))
    country = cur.fetchone()
    if country is None:
        return jsonify({'error': 'Country not found'}), 404
    return jsonify(country), 200

#task3
@app.route('/api/auth/register', methods=['POST'])
def register_user():
    if not all(k in request.json for k in ['username', 'password', 'email']):
        return jsonify({'error': 'Missing fields'}), 400
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (request.json['email']))
    if cur.fetchone() is not None:
        return jsonify({'error': 'Current email already exists'}), 400

    if len(request.json['password']) < 8:
        return jsonify({'error': 'Password length must be at least 8 characters'}), 400

    password_hash =bcrypt.generate_password_hash(request.json['password'])
    cur = conn.cursor()
    (cur.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s"),
     (request.json['username'], password_hash, request.json['email']))
    conn.commit()
    return jsonify({'message': 'User was registered successfully'}), 201

#task4


if __name__ == "__main__":
    app.run(host=SERVER_ADDRESS, port=SERVER_PORT)
