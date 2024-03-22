import requests

from django.db import models
from django.utils.html import format_html


# Create your models here.
class User(models.Model):
    chat_id = models.CharField(max_length=40, unique=True)
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'chat_id']),
            models.Index(fields=['-created_at'])
        ]

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
    
    def __str__(self) -> str:
        return self.title

class Unit(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
    
    def __str__(self) -> str:
        return self.title


# Passage class
class Passage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['title']
    
    def __str__(self) -> str:
        return self.title


class VocabularyManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related('book')  # Optimize for performance

    def for_book(self, book):
        return self.get_queryset().filter(book=book)


class Vocabulary(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE)
    objects = VocabularyManager()
    word = models.CharField(max_length=500)
    definition = models.CharField(max_length=500)
    translated = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['word']

    def __str__(self):
        return self.word



class Test(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=1)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    passages = models.ManyToManyField(Passage, related_name='test_passages')
    total = models.IntegerField(default=0)

    def __str__(self):
        return f"Test for Unit {self.unit}"

class VocabularyTraining(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.SmallIntegerField(default=0)
    correct = models.SmallIntegerField(default=0)
    wrong = models.SmallIntegerField(default=0)
    result = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return self.user.name


class Homework(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, default="images/nophoto.jpg")
    image_url = models.CharField(max_length=255)
    caption = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return " ,".join([self.image_url, self.caption,str(self.date)])
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the instance is being created (not updated)
            if self.image and not self.image_url:
                # Call your function to upload photo to AWS S3 and get the URL
                uploaded_image_url = self.upload_to_telegraph(self.image)

                # Update the image_url field with the URL returned from AWS S3
                self.image_url = uploaded_image_url
        super().save(*args, **kwargs)

    def upload_to_telegraph(self, image_file):
            YOUR_TELEGRAPH_ACCESS_TOKEN = "81054b18bfbeb455da67c3e8f1dd0eba6dda7a9153e11030f5dfcf6d5050"
            url = 'https://telegra.ph/upload'

            files = {
                'file': image_file.file  # Pass the file object from the ImageField
            }

            headers = {
                'Authorization': f'Bearer {YOUR_TELEGRAPH_ACCESS_TOKEN}'  # Replace with your Telegra.ph access token
            }

            response = requests.post(url, files=files, headers=headers)
            
            if response.status_code == 200:
                response_data = response.json()
                # Image uploaded successfully, extract the URL
                image_url = f"https://telegra.ph{response_data[0]['src']}"
                print(image_url)
                return image_url
            else:
                # Handle upload error
                print("Image upload failed:", response_data)
                return None
