'''
API Resource for blog manipulations
'''
from flask import request, g
from flask_restful import Resource
from werkzeug.exceptions import abort
from nonie_server.api.v1.resources.user import login_required
from nonie_server.db import get_db


class Create(Resource):
    '''
    A class representing a create resource.

    Attributes:
        None

    Methods:
        post(): create a new post.
    '''
    @login_required
    def post(self):
        '''
        Handles HTTP POST request to create a new post.

        Returns:
            dict: A dictionary with the message of success or error.
        '''
        title = request.form['title']
        body = request.form['body']

        if not title:
            return {'message': 'Title is required.'}

        db = get_db()
        db.execute(
            'INSERT INTO post (title, body, author_id)'
            ' VALUES (?, ?, ?)',
            (title, body, g.user['id'])
        )
        db.commit()
        return {'message': 'Create post successfully!'}


def get_post(post_id, check_author=True):
    '''
    Get a post by its ID.

    Parameters:
        post_id: The ID of the post.
        check_author: A boolean indicating whether to check the author of the post.

    Returns:
        The post if found, otherwise raise a 404 error.
    '''
    post = get_db().execute(f'''
        SELECT p.id, title, body, created, author_id, username
        FROM post p JOIN user u ON p.author_id = u.id
        WHERE p.id = {post_id};
    '''
    ).fetchone()

    if post is None:
        abort(404, f"Post id {post_id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


class Blog(Resource):
    '''
    A class representing a blog resource.

    Attributes:
        None

    Methods:
        get(post_id): Retrieve a specific post by its ID.
        put(post_id): Update a specific post by its ID.
        delete(post_id): Delete a specific post by its ID.
    '''
    def get(self, post_id):
        '''
        Retrieve a specific post by its ID.

        Args:
            post_id (int): The ID of the post to retrieve.

        Returns:
            dict: A dictionary containing a message and the retrieved post.
        '''
        post = get_post(post_id)
        return {
            'message': 'Get post successfully!',
            'post': post
        }

    @login_required
    def put(self, post_id):
        '''
        Update a specific post by its ID.

        Args:
            post_id (int): The ID of the post to update.

        Returns:
            dict: A dictionary containing a message indicating the update status.
        '''
        get_post(post_id)
        title = request.form['title']
        body = request.form['body']

        if not title:
            return {'message': 'Title is required.'}

        db = get_db()
        db.execute(
            'UPDATE post SET title = ?, body = ?'
            ' WHERE id = ?',
            (title, body, post_id)
        )
        db.commit()
        return {'message': 'Update post successfully!'}

    @login_required
    def delete(self, post_id):
        '''
        Delete a specific post by its ID.

        Args:
            post_id (int): The ID of the post to delete.

        Returns:
            dict: A dictionary containing a message indicating the delete status.
        '''
        get_post(post_id)
        db = get_db()
        db.execute('DELETE FROM post WHERE id = ?', (post_id,))
        db.commit()
        return {'message': 'Delete post successfully!'}
