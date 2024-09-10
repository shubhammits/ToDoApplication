from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add_todo', methods=['POST'])
def add_todo():
    new_task = {
        'id': len(tasks) + 1,
        'task': request.form['task'],
        'completed': False,
        'priority': request.form['priority'],
        'due_date': request.form.get('due_date')
    }
    tasks.append(new_task)
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        task['completed'] = True
    return redirect(url_for('index'))

@app.route('/not_completed/<int:task_id>')
def not_completed_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        task['completed'] = False
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET'])
def edit_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    return render_template('edit_task.html', task=task)

@app.route('/edit_task/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        task['task'] = request.form['task']
        task['due_date'] = request.form.get('due_date')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
