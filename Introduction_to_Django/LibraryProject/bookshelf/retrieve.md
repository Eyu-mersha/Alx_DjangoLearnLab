books = Book.objects.all()
  for book in books:
      print(book.title, book.author, book.publication_year)

"Book.objects.get", "1984"