from django.contrib import admin
from .models import Letter, SentLetter

@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'email', 'created',)

@admin.register(SentLetter)
class SentLetterAdmin(admin.ModelAdmin):
    list_display = ('letter', 'sent_date',)
