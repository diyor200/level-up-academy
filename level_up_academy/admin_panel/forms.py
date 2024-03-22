from django import forms

from .models import Homework, Unit, Passage, Vocabulary, Book

class HomeworkAdminForm(forms.ModelForm):
    class Meta:
        model = Homework
        exclude = ['image_url']


class VocabularyAdminForm(forms.ModelForm):
    class Meta:
        model = Vocabulary
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unit'].queryset = Unit.objects.none()
        self.fields['passage'].queryset = Passage.objects.none()

        # Handle book selection for unit & passage filtering
        if 'book' in self.initial:
            book = self.initial['book']
            self.fields['unit'].queryset = book.unit_set.all()

    def clean(self):
        cleaned_data = super().clean()
        book = cleaned_data.get('book')
        unit = cleaned_data.get('unit')

        # Ensure unit belongs to the chosen book
        if unit and book and unit.book != book:
            raise forms.ValidationError("Selected unit does not belong to the chosen book.")

        return cleaned_data