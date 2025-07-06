from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        counter = 0
        tags = []
        for form in self.forms:
            for key, value in form.cleaned_data.items():
                print(key, value)
                if key == 'is_main' and value is True:
                    counter += 1
                if key == 'tag':
                    if value not in tags:
                        tags.append(value)
                    else:
                        raise ValidationError('Этот тег уже добавлен')
        if counter > 1:
            raise ValidationError('Основной раздел может быть только один')
        elif counter == 0:
            raise ValidationError('Укажите основной раздел')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'published_at']
    list_filter = ['published_at']
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['id', 'name']
