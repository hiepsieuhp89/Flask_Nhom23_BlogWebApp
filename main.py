from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__,
            static_url_path='', 
            static_folder='templates/assets',
            template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)
class CodeSpeedyBlog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    posted_by = db.Column(db.String(20), nullable=False, default='N/A')
    posted_on = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow())
    def __repr__(self):
        return self.title
db.create_all()
db.session.commit()

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/')
@app.route('/home')
@app.route('/CodeSpeedy')
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['post']
        post_author = request.form['author']
        new_post = CodeSpeedyBlog(title=post_title,
                        content=post_content, posted_by=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = CodeSpeedyBlog.query.order_by(CodeSpeedyBlog.posted_on).all()
        return render_template('index.html', posts=all_posts)

@app.route('/post',  methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['post']
        post_author = request.form['author']
        new_post = CodeSpeedyBlog(title=post_title,
                        content=post_content, posted_by=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/')
    else:
        p_id = request. args. get("id")
        post = CodeSpeedyBlog.query.get(p_id)
        return render_template('post.html', post=post)

@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['post']
        post_author = request.form['author']
        new_post = CodeSpeedyBlog(title=post_title,
                        content=post_content, posted_by=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('new_post.html')
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    to_edit = CodeSpeedyBlog.query.get_or_404(id)
    if request.method == 'POST':
        to_edit.title = request.form['title']
        to_edit.author = request.form['author']
        to_edit.content = request.form['post']
        db.session.commit()
        return redirect('/')
    else:
        return render_template('edit.html', post=to_edit)
@app.route('/posts/delete/<int:id>')
def delete(id):
    to_delete = CodeSpeedyBlog.query.get_or_404(id)
    db.session.delete(to_delete)
    db.session.commit()
    return redirect('/')
if __name__ == "__main__":
    app.run(debug=True)
