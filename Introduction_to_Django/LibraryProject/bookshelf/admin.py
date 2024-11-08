from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add search functionality
    search_fields = ('title', 'author')
    
    # Add filter for publication_year
    list_filter = ('publication_year',)

# Register the custom admin class
admin.site.register(Book, BookAdmin)