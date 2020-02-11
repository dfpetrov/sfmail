from django.db import models

class Letter(models.Model):
    subject = models.CharField(null=False, blank=False, max_length=100)
    email = models.EmailField(null=False, blank=False)
    message = models.TextField(null=False, blank=False, max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    delay = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'

    def __str__(self):
        return f'{self.email} ({self.created})'

class SentLetter(models.Model):
    letter = models.ForeignKey(Letter, null=True, blank=True, on_delete=models.CASCADE)
    sent_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='не отправлено')

    class Meta:
        verbose_name = 'Отправленное письмо'
        verbose_name_plural = 'Отправленные письма'

    def __str__(self):
        return f'{self.letter} ({self.sent_date})'