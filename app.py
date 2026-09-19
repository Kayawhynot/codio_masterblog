"""Flask blog application with JSON file persistence.

Provides CRUD operations for blog posts: create, read, update, delete.
Posts are stored as a list of dictionaries in posts.json.
"""

from flask import Flask, render_template, request, url_for, redirect
import json

app = Flask(__name__)


@app.route('/')
def index():
    """Display all blog posts on the homepage.

    Reads all posts from posts.json and renders them via index.html.
    """
    with open('posts.json', 'r') as file:
        blog_posts = json.load(file)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Display the add-post form (GET) or create a new post (POST).

    On POST: reads form data (author, title, content), assigns a new
    unique id, appends the post to posts.json, and redirects to index.
    On GET: renders the empty add.html form.
    """
    if request.method == 'POST':
        with open('posts.json', 'r') as file:
            blog_posts = json.load(file)

        all_ids = []
        for post in blog_posts:
            all_ids.append(post['id'])
        if not all_ids:
            new_id = 1
        else:
            new_id = max(all_ids) + 1

        new_post = {
            "id": new_id,
            "author": request.form.get('author'),
            "title": request.form.get('title'),
            "content": request.form.get('content')
        }

        blog_posts.append(new_post)

        with open('posts.json', 'w') as file:
            json.dump(blog_posts, file)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Delete the post with the given id and redirect to index.

    Returns a 404 if no post with this id exists.
    """
    post = fetch_post_by_id(post_id)
    if post is None:
        return 'Post not found', 404

    with open('posts.json', 'r') as file:
        blog_posts = json.load(file)

    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            break

    with open('posts.json', 'w') as file:
        json.dump(blog_posts, file)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Display the update form (GET) or save changes to a post (POST).

    Returns a 404 if no post with this id exists. On POST, overwrites
    author, title and content with the submitted form values and
    redirects to index.
    """
    post = fetch_post_by_id(post_id)
    if post is None:
        return 'Post not found', 404

    if request.method == 'POST':
        with open('posts.json', 'r') as file:
            blog_posts = json.load(file)

        for post in blog_posts:
            if post['id'] == post_id:
                post['author'] = request.form.get('author')
                post['title'] = request.form.get('title')
                post['content'] = request.form.get('content')
                break

        with open('posts.json', 'w') as file:
            json.dump(blog_posts, file)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


def fetch_post_by_id(post_id):
    """Return the post dict with the given id, or None if not found."""
    with open('posts.json', 'r') as file:
        all_posts = json.load(file)
        for post in all_posts:
            if post['id'] == post_id:
                return post
        return None


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
