from django.core.mail import send_mail

from blog.models import Post
from project.celery import app
from project.model_choices import Status

@app.task
def send_email_task(post_id, cd):
    post = Post.objects.get(id=post_id, status=Status.PUBLISHED)
    post_url = post.get_absolute_url()
    subject = f"{cd['name']} recommends you read {post.title}"
    message = f"Read {post.title} at {post_url}\n\n" \
              f"{cd['name']}'s comments: {cd['comments']}"
    send_mail(subject, message, 'your_account@gmail.com', [cd['to']])