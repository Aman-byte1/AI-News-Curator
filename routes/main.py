from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, NewsArticle, UserInteraction, Comment # Import Comment
from forms import NewsArticleForm, CommentForm # Import CommentForm
from sqlalchemy import desc

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index')
@login_required
def index():
    """
    Displays the main news feed with interaction counts.
    """
    articles = NewsArticle.query.order_by(desc(NewsArticle.posted_at)).all()
    articles_with_data = []
    for article in articles:
        # Calculate interaction counts for each article
        likes_count = UserInteraction.query.filter_by(article_id=article.id, interaction_type='liked').count()
        dislikes_count = UserInteraction.query.filter_by(article_id=article.id, interaction_type='disliked').count()
        shares_count = UserInteraction.query.filter_by(article_id=article.id, interaction_type='shared').count()
        # Get comment count for each article
        comments_count = Comment.query.filter_by(article_id=article.id).count()

        articles_with_data.append({
            'article': article,
            'likes_count': likes_count,
            'dislikes_count': dislikes_count,
            'shares_count': shares_count,
            'comments_count': comments_count, # Add comments count
        })
    return render_template('news/index.html', title='News Feed', articles_with_data=articles_with_data)


@main_bp.route('/article/<int:article_id>', methods=['GET', 'POST']) # Allow POST for comments
@login_required
def article(article_id):
    """
    Displays a single news article, records a 'read' interaction,
    and handles comment submission.
    """
    article = NewsArticle.query.get_or_404(article_id)
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        comment = Comment(
            content=comment_form.content.data,
            article_id=article.id,
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        print(f"Comment posted by {current_user.username} on article {article.id}: {comment.content}") # Debug print
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('main.article', article_id=article.id))

    # Record user interaction: 'read' (only on GET request to avoid re-recording on comment post)
    if request.method == 'GET':
        # Check if this specific 'read' interaction already exists to prevent duplicates
        existing_read = UserInteraction.query.filter_by(
            user_id=current_user.id,
            article_id=article.id,
            interaction_type='read'
        ).first()
        if not existing_read:
            interaction = UserInteraction(
                user_id=current_user.id,
                article_id=article.id,
                interaction_type='read'
            )
            db.session.add(interaction)
            db.session.commit()
            print(f"Read interaction recorded for user {current_user.username} on article {article.id}") # Debug print
            flash(f"You read '{article.title}'. This interaction helps personalize your feed!", 'info')

    # Get interaction counts for the specific article
    likes_count = UserInteraction.query.filter_by(article_id=article.id, interaction_type='liked').count()
    dislikes_count = UserInteraction.query.filter_by(article_id=article.id, interaction_type='disliked').count()
    shares_count = UserInteraction.query.filter_by(article_id=article.id, interaction_type='shared').count()

    # Fetch comments for the article, ordered by most recent
    comments = Comment.query.filter_by(article_id=article.id).order_by(desc(Comment.posted_at)).all()

    return render_template('news/article.html',
                           title=article.title,
                           article=article,
                           likes_count=likes_count,
                           dislikes_count=dislikes_count,
                           shares_count=shares_count,
                           comments=comments,
                           comment_form=comment_form)

@main_bp.route('/news/new', methods=['GET', 'POST'])
@login_required
def create_news():
    """
    Allows approved media users and admin users to post new news articles.
    """
    # Only media or admin users can post news
    if current_user.role not in ['media', 'admin']:
        flash('You do not have permission to post news.', 'danger')
        return redirect(url_for('main.index'))

    form = NewsArticleForm()
    if form.validate_on_submit():
        article = NewsArticle(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            source_name=form.source_name.data,
            source_url=form.source_url.data,
            user_id=current_user.id # Associate article with the current media/admin user
        )
        db.session.add(article)
        db.session.commit()
        print(f"Article '{article.title}' posted by user {current_user.username}. Article ID: {article.id}") # Debug print
        flash('Your news article has been posted!', 'success')
        return redirect(url_for('main.index'))
    return render_template('news/create_news.html', title='Post New Article', form=form)

@main_bp.route('/interact/<int:article_id>/<interaction_type>')
@login_required
def record_interaction(article_id, interaction_type):
    """
    Records various user interactions (like, dislike, share, skip) with count updates.
    """
    article = NewsArticle.query.get_or_404(article_id)
    valid_interactions = ['liked', 'disliked', 'shared', 'skipped']

    if interaction_type not in valid_interactions:
        flash('Invalid interaction type.', 'danger')
        return redirect(url_for('main.article', article_id=article.id))

    # Check if user already performed this interaction
    existing_interaction = UserInteraction.query.filter_by(
        user_id=current_user.id,
        article_id=article.id,
        interaction_type=interaction_type
    ).first()

    if existing_interaction:
        # For like/dislike, allow toggle (remove interaction)
        if interaction_type in ['liked', 'disliked']:
            db.session.delete(existing_interaction)
            db.session.commit()
            print(f"Removed {interaction_type} interaction for user {current_user.username} on article {article.id}") # Debug print
            flash(f"You've removed your {interaction_type} interaction.", 'info')
        else:
            flash(f"You've already recorded this interaction for '{article.title}'.", 'info')
    else:
        # For like/dislike, remove opposite interaction if exists
        if interaction_type in ['liked', 'disliked']:
            opposite_type = 'disliked' if interaction_type == 'liked' else 'liked'
            opposite_interaction = UserInteraction.query.filter_by(
                user_id=current_user.id,
                article_id=article.id,
                interaction_type=opposite_type
            ).first()

            if opposite_interaction:
                db.session.delete(opposite_interaction)
                print(f"Removed opposite ({opposite_type}) interaction for user {current_user.username} on article {article.id}") # Debug print

        # Create new interaction
        interaction = UserInteraction(
            user_id=current_user.id,
            article_id=article.id,
            interaction_type=interaction_type
        )
        db.session.add(interaction)
        db.session.commit()
        print(f"Added {interaction_type} interaction for user {current_user.username} on article {article.id}") # Debug print
        flash(f"Interaction '{interaction_type}' recorded!", 'success')

    return redirect(request.referrer or url_for('main.index'))