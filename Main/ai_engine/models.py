from django.db import models

# Create your models here.

class GrammarCache(models.Model):
    original_text = models.TextField(unique=True)
    corrected_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_text[:50]