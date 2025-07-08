from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, NewsArticle, UserInteraction
from forms import NewsArticleForm
from sqlalchemy import desc

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index')
@login_required
def index():
    """
    Displays the main news feed.
    This is where AI personalization would conceptually integrate.
    For now, it shows all articles ordered by most recent.
    """
    # In a real AI system, this query would be replaced by AI recommendations.
    # Example: articles = ai_service.get_personalized_news(current_user.id)
    articles = NewsArticle.query.order_by(desc(NewsArticle.posted_at)).all()
    return render_template('news/index.html', title='News Feed', articles=articles)

@main_bp.route('/article/<int:article_id>')
@login_required
def article(article_id):
    """
    Displays a single news article and records a 'read' interaction.
    """
    article = NewsArticle.query.get_or_404(article_id)

    # Record user interaction: 'read'
    interaction = UserInteraction(
        user_id=current_user.id,
        article_id=article.id,
        interaction_type='read'
    )
    db.session.add(interaction)
    db.session.commit()
    flash(f"You read '{article.title}'. This interaction helps personalize your feed!", 'info')

    return render_template('news/article.html', title=article.title, article=article)

@main_bp.route('/news/new', methods=['GET', 'POST'])
@login_required
def create_news():
    """
    Allows approved media users to post new news articles.
    """
    # Only media users can post news
    if current_user.role != 'media':
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
            user_id=current_user.id # Associate article with the current media user
        )
        db.session.add(article)
        db.session.commit()
        flash('Your news article has been posted!', 'success')
        return redirect(url_for('main.index'))
    return render_template('news/create_news.html', title='Post New Article', form=form)

@main_bp.route('/interact/<int:article_id>/<interaction_type>')
@login_required
def record_interaction(article_id, interaction_type):
    """
    Records various user interactions (like, dislike, share, skip).
    """
    article = NewsArticle.query.get_or_404(article_id)

    # Ensure interaction type is valid
    valid_interactions = ['liked', 'disliked', 'shared', 'skipped']
    if interaction_type not in valid_interactions:
        flash('Invalid interaction type.', 'danger')
        return redirect(url_for('main.article', article_id=article.id))

    # Check if an interaction of this type already exists for this user and article
    existing_interaction = UserInteraction.query.filter_by(
        user_id=current_user.id,
        article_id=article.id,
        interaction_type=interaction_type
    ).first()

    if existing_interaction:
        flash(f"You've already recorded this interaction for '{article.title}'.", 'info')
    else:
        interaction = UserInteraction(
            user_id=current_user.id,
            article_id=article.id,
            interaction_type=interaction_type
        )
        db.session.add(interaction)
        db.session.commit()
        flash(f"Interaction '{interaction_type}' recorded for '{article.title}'. This helps personalize your feed!", 'success')

    return redirect(request.referrer or url_for('main.index')) # Redirect back to where they came from