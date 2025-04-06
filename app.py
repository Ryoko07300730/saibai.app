from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# 🔹 データベースの初期化（テーブルを作る）
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            memo TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 🔹 トップページ（登録フォーム＆一覧を表示）
@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM plants')  # 全データ取得
    plants = c.fetchall()
    conn.close()
    return render_template('index.html', plants=plants)

# 🔹 植物データを追加
@app.route('/add', methods=['POST'])
def add_plant():
    plant_name = request.form['plant_name']
    plant_date = request.form['plant_date']
    plant_memo = request.form['plant_memo']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO plants (name, date, memo) VALUES (?, ?, ?)', 
              (plant_name, plant_date, plant_memo))
    conn.commit()
    conn.close()
    return redirect('/')

# 🔹 植物データを削除
@app.route('/delete/<int:plant_id>', methods=['POST'])
def delete_plant(plant_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM plants WHERE id = ?', (plant_id,))
    conn.commit()
    conn.close()
    return redirect('/')

# 🔹 Flaskアプリを実行
if __name__ == '__main__':
    app.run(debug=True)
