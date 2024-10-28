from django.db import models

class Message(models.Model):
    SENDER_CHOICES = [
        ('customer', 'Customer'),
        ('agent', 'Agent'),
    ]
    
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    content = models.TextField()
    translated_content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.content[:50]}"  # Display the first 50 characters of the message
