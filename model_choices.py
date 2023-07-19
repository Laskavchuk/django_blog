from django.db.models import  TextChoices

class Status(TextChoices):
    DRAFT = 'DF', 'Draft'

    PUBLISHED = 'PB', 'Published'