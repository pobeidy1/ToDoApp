from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date_created TEXT NOT NULL,
            date_completed TEXT,
            progress INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subtasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            date_created TEXT NOT NULL,
            date_completed TEXT,
            done BOOLEAN DEFAULT FALSE,
            FOREIGN KEY(task_id) REFERENCES tasks(id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
        return jsonify(tasks)

    if request.method == 'POST':
        data = request.json
        cursor.execute(
            'INSERT INTO tasks (title, date_created, progress) VALUES (?, ?, ?)',
            (data['title'], data['date_created'], 0)
        )
        conn.commit()
        return jsonify({'status': 'Task added successfully'})

@app.route('/subtasks', methods=['POST'])
def add_subtask():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    data = request.json
    cursor.execute(
        'INSERT INTO subtasks (task_id, title, date_created, done) VALUES (?, ?, ?, ?)',
        (data['task_id'], data['title'], data['date_created'], False)
    )
    conn.commit()
    return jsonify({'status': 'Subtask added successfully'})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    cursor.execute('DELETE FROM subtasks WHERE task_id = ?', (task_id,))
    conn.commit()
    return jsonify({'status': 'Task deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
