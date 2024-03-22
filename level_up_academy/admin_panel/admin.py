from django.contrib import admin
from django.utils.html import format_html

from .models import User, VocabularyTraining, Vocabulary, Homework, Test, Passage, Book, Unit
from .forms import HomeworkAdminForm, VocabularyAdminForm


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']

@admin.register(Passage)
class PassageAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit', 'created_at', 'updated_at']


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['__str__']


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'phone', 'chat_id']
    list_filter = ['name', 'username']
    search_fields = ['name', 'username', 'phone', 'chat_id']


@admin.register(Vocabulary)
class VocabularyAdmin(admin.ModelAdmin):
    form = VocabularyAdminForm
    list_display = ['word', 'definition', 'translated']
    list_filter = ['word', 'definition', 'translated']
    search_fields = ['word', 'definition', 'translated']


@admin.register(VocabularyTraining)
class VocabularyTrainingAdmin(admin.ModelAdmin):
    list_display = ['user', 'total', 'correct', 'wrong', 'created_at']
    list_filter = ['user', 'total', 'correct', 'wrong', 'created_at']
    search_fields = ['user', 'total', 'correct', 'wrong', 'created_at']


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    # Define a form for adding new instances
    def get_form(self, request, obj=None, **kwargs):
        # Exclude 'image_url' field from the add form
        if obj is None:
            kwargs['form'] = HomeworkAdminForm
        else:
            self.exclude = ()
        
        return super().get_form(request, obj, **kwargs)
    
    def thumbnail(self, object):
        
        try:
            url = object.image.url
        except:
            url = '/media/images/nophoto.jpg'
        
        return format_html(f'<img src="{url}" width="40" style="border-radius: 50px;" />')
    thumbnail.short_description = 'Homework Image'
    list_display = ['caption', 'thumbnail' ,'date']
    list_filter = ['caption', 'date']
    search_fields = ['caption', 'date']

