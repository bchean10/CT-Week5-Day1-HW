from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from . import bp as data
from .models import Comment, PokeData

@data.route('/', methods = ['GET'])
@login_required
def index():
    return render_template('index.html.j2')

@data.route('/pokedata', methods=['GET', 'POST'])
@login_required
def pokedata():
    pokes = PokeData.query.all()
    if request.method == 'POST':
        body_from_form = request.form.get('body')
        poke_id = request.args.get('pokemon_id')
        try:
            new_comment = Comment(body=body_from_form, user_id=current_user.id, pokemon_id=poke_id)
            new_comment.save()
            flash(f"Successfully commented!", "success")
            return redirect(url_for('data.pokedata'))
        except:
            flash(f"Error commenting on pokemon. Please try again!", "warning")
            return redirect(url_for('data.pokedata'))
    return render_template('poke_data.html.j2', data=pokes)

@data.route('/comment/my_comment', methods=['GET'])
@login_required
def my_comment():
    print(current_user.comment)
    return render_template('my_comment.html.j2', comments=current_user.comment)

@data.route('/comment/<int:id>', methods=['GET'])
@login_required
def get_comment(id):
    comment = Comment.query.get(id)
    return render_template('my_comment.html.j2', comment=comment, view_all=True)

@data.route('/edit_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_comment():
    comment = Comment.query.get(id)
    if request.method == 'POST':
        if current_user.id==comment.user_id:
            comment.edit(request.form.get("body"))
            flash("Your comment has been edited", "success")
        else:
            flash("Edit fail!", "warning")
        return redirect(url_for('data.edit_comment'))
    return render_template('edit_comment.html.j2',comment=comment)

@data.route('/delete_comment/<int:id>', methods=['GET'])
@login_required
def delete_comment():
    comment_to_delete = Comment.query.get(id)
    if current_user.id==comment_to_delete.user_id:
        comment_to_delete.delete()
        flash("Your comment has been deleted", "info")
    else:
        flash("Delete Fail!", "warning")
    return redirect(url_for('data.pokedata'))