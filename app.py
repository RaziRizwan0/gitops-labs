import os, sqlite3
from flask import Flask, jsonify, request, render_template_string, redirect
app = Flask(__name__)
DB_PATH = os.environ.get('DATABASE_PATH', '/tmp/names.db')
os.makedirs(os.path.dirname(DB_PATH) or '.', exist_ok=True)
PAGE = '''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>GitOps Labs</title><style>body{font-family:system-ui;max-width:760px;margin:3rem auto;padding:0 1rem;color:#172033}.card{border:1px solid #d8deea;border-radius:14px;padding:1.25rem;margin:1rem 0}input,button{font:inherit;padding:.7rem;border-radius:8px;border:1px solid #aab4c5}button{background:#172033;color:white}li{padding:.25rem}.muted{color:#657086}</style></head><body><h1>GitOps Labs</h1><p class="muted">A demo app for CI/CD, Kubernetes and GitOps delivery.</p><div class="card"><form method="post" action="/names"><label for="name">Add a name</label><br><br><input id="name" name="name" maxlength="100" required placeholder="Enter a name"><button type="submit">Save</button></form></div><div class="card"><h2>Saved names ({{ names|length }})</h2>{% if names %}<ul>{% for name in names %}<li>{{ name }}</li>{% endfor %}</ul>{% else %}<p>No names yet. Add the first one above.</p>{% endif %}</div><p class="muted">Health: <a href="/healthz">/healthz</a> · API: <a href="/api/names">/api/names</a></p></body></html>'''
def connect():
    db=sqlite3.connect(DB_PATH, timeout=10); db.execute('CREATE TABLE IF NOT EXISTS names (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)'); return db
@app.get('/')
def index():
    with connect() as db: names=[r[0] for r in db.execute('SELECT name FROM names ORDER BY id DESC').fetchall()]
    return render_template_string(PAGE, names=names)
@app.post('/names')
def create_name():
    name=(request.form.get('name') or '').strip()
    if not name or len(name)>100: return 'Name must be 1-100 characters',400
    with connect() as db: db.execute('INSERT INTO names(name) VALUES (?)',(name,))
    return redirect('/', code=303)
@app.get('/api/names')
def list_names():
    with connect() as db: rows=db.execute('SELECT id,name,created_at FROM names ORDER BY id DESC').fetchall()
    return jsonify([{'id':r[0],'name':r[1],'created_at':r[2]} for r in rows])
@app.get('/healthz')
def healthz():
    try:
        with connect() as db: db.execute('SELECT 1')
        return jsonify(status='ok')
    except sqlite3.Error: return jsonify(status='error'),500
