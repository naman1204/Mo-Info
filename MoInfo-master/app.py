from flask import Flask, render_template, url_for, request, redirect
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#db = SQLAlchemy(app)

#class Todo(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    owner = db.Column(db.String(20), nullable=False)
#    coursecode = db.Column(db.String(20), nullable=False)
#    groupname = db.Column(db.String(20), nullable=False, unique=True)
#    members = db.Column(db.String(20), nullable=False)
#
#
#    def __repr__(self):
#        return '<Task %r>' % self.id

class ghetto_db:
    def __init__(self) -> None:
        self.db = {}
        self.id_count = 0
    
    # Group owner actions:
    def add_group(self, owner: str, groupname: str, coursecode: str) -> dict:
        group_id = coursecode+str(self.id_count)
        self.db[group_id] = {'group_id': group_id, 'owner': owner, 'groupname': groupname, 'coursecode': coursecode, 'members': []}
        self.id_count += 1
        return group_id
    
    def delete_group(self, group_id: str) -> None:
        if group_id in self.db:
            del self.db[group_id]
   
    # Group memebr actions:
    def group_info(self, group_id: str) -> dict:
        return (self.db).get(group_id, {'group_id': group_id, 'owner': 'ERROR', 'groupname': 'ERROR', 'coursecode': 'ERROR', 'members': []})


    def find_data(self, coursecode: str) -> list:
        found = []
        for group_id in self.db:
            if coursecode in group_id:
                found.append(self.db[group_id])
        return found
    
    def join_group(self, group_id: str, memeber: str) -> None:
        if group_id in self.db:
            (self.db[group_id]['members']).append(memeber)

    def leave_group(self, group_id: str, member: str) -> None:
        if group_id in self.db:
            (self.db[group_id]['members']).remove(member)


db = ghetto_db()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        group_id = db.add_group(request.form['username'], request.form['groupname'], request.form['coursecode'])
        return redirect(f'/group/{group_id}')
    else:
        return render_template('create.html')
    
@app.route('/group/<group_id>')
def created_group(group_id):
    data = db.group_info(group_id)
    return render_template('groupowner.html', data=data)

    
@app.route('/deletegroup/<group_id>')
def delete(group_id):
    db.delete_group(group_id)
    return redirect('/')

@app.route('/find', methods=['POST', 'GET'])
def find():
    if request.method == 'POST':
        data = db.find_data(request.form['coursecode'])
        username = request.form['username']
        return render_template('listgroup.html', data=data, username=username)
    else:
        return render_template('find.html')
    
@app.route('/join/<username>/<group_id>')
def join(username, group_id):
    db.join_group(group_id, username)
    return redirect(f'/joinedgroup/{username}/{group_id}') 

@app.route('/joinedgroup/<username>/<group_id>')
def joinedgroup(username, group_id):
    data = db.group_info(group_id)
    return render_template('joinedgroup.html', data=data, username=username)

@app.route('/leavegroup/<username>/<group_id>')
def leavegroup(username, group_id):
    db.leave_group(group_id, username)
    return redirect('/')

@app.route('/notes')
def notes():
    return render_template('notes.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run()