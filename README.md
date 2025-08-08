# **Blog-Django-API**

This is a Django REST Framework project. On the home page, you can learn more about the project. The main focus of the project is the API. Visit the [API root list of endpoints](/api/) to see all URLs and their allowed methods. You will need Postman or another tool to make API requests using different methods. Some URLs require login. The token can be sent in the headers or in the authorization field (in Postman). You can view all registered users on this page below. You can visit the GET URLs by clicking the links provided below.

## Technology:

- Python
- Django Rest Framework (DRF)
- JWT Authentication (Simple JWT - library)
- SQLite
- Unit Tests

## Features:

1. **User Authentication**: 
   - Register and log in users with JWT tokens for secure authentication. You can paste the token in the headers. You can also refresh the token to obtain a new access token.
   
2. **CRUD Operations**: 
   - Create, read, update, and delete blog posts, comments, and authors.
   
3. **Comments**: 
   - Users can comment on posts, and comments are linked to specific posts and authors.
   
4. **Search and Ordering**: 
   - Filter and sort posts by title or body content.
   
5. **Rate Limiting**: 
   - Limits for unauthenticated users to prevent abuse.
   
6. **Pagination**: 
   - Get posts in a paginated format to handle large datasets efficiently.
   
7. **Admin Interface**: 
   - Easy management of posts, authors, and comments through Django’s built-in admin interface.
