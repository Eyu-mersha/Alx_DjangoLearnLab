from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import Book, Author

class BookAPITests(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Create an Author
        cls.author = Author.objects.create(name="J.K. Rowling")
        
        # Create books
        cls.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=cls.author
        )
        cls.book2 = Book.objects.create(
            title="Harry Potter and the Chamber of Secrets",
            publication_year=1998,
            author=cls.author
        )

    def test_create_book(self):
        # Test that a new book can be created
        url = reverse('book-list')  # Adjust the URL name based on your urls.py
        data = {
            'title': 'Harry Potter and the Prisoner of Azkaban',
            'publication_year': 1999,
            'author': self.author.id
        }
        response = self.client.post(url, data, format='json')
        
        # Check if the response is a successful status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify the new book exists in the database
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(response.data['title'], 'Harry Potter and the Prisoner of Azkaban')

    def test_list_books(self):
        # Test that the book list is retrievable
        url = reverse('book-list')  # Adjust the URL name based on your urls.py
        response = self.client.get(url)
        
        # Check if the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if the correct number of books is returned
        self.assertEqual(len(response.data), 2)

    def test_get_book_detail(self):
        # Test that the book detail endpoint returns correct data
        url = reverse('book-detail', kwargs={'pk': self.book1.id})  # Adjust URL name and kwargs
        response = self.client.get(url)
        
        # Check if the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify that the correct book is returned
        self.assertEqual(response.data['title'], self.book1.title)

    def test_update_book(self):
        # Test updating a book's details
        url = reverse('book-detail', kwargs={'pk': self.book1.id})  # Adjust URL name and kwargs
        data = {
            'title': 'Harry Potter and the Philosopher\'s Stone (Updated)',
            'publication_year': 2000,
            'author': self.author.id
        }
        response = self.client.put(url, data, format='json')
        
        # Check if the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify that the book was updated
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Harry Potter and the Philosopher\'s Stone (Updated)')
        
    def test_delete_book(self):
        # Test deleting a book
        url = reverse('book-detail', kwargs={'pk': self.book1.id})  # Adjust URL name and kwargs
        response = self.client.delete(url)
        
        # Check if the response is successful
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify the book has been deleted
        self.assertEqual(Book.objects.count(), 1)  # One book should be left

    def test_permissions(self):
        # Test that only authenticated users can create, update, or delete books
        
        # Create a new user and get token
        user = self.create_user()  # Assuming you have a utility method to create users
        token = Token.objects.create(user=user)
        self.client.login(HTTP_AUTHORIZATION='Token ' + token.key)
        
        # Create a book with authentication
        url = reverse('book-list')
        data = {
            'title': 'Harry Potter and the Goblet of Fire',
            'publication_year': 2000,
            'author': self.author.id
        }
        response = self.client.post(url, data, format='json')
        
        # Ensure the response is successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test without authentication (should fail)
        self.client.login()  # Clear login
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_filter_books_by_title(self):
        # Test filtering books by title
        url = reverse('book-list')  # Adjust the URL name based on your urls.py
        response = self.client.get(url, {'title': 'Harry Potter'})
        
        # Check if the filtering works correctly
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # We should have 2 books with "Harry Potter" in the title

    def test_ordering_books_by_title(self):
        # Test ordering books by title
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        # Check if the books are ordered by title
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Harry Potter and the Chamber of Secrets')  # Alphabetically first

