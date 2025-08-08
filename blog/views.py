from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import Post, Author, Comment
from .serializers import PostSerializer, AuthorSerializer, CommentSerializer, UserSerializer

from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.filters import SearchFilter, OrderingFilter


class PostList(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'body']
    # http://127.0.0.1:8000/api/posts/?search=something

    ordering_fields = ['title']
    # http://127.0.0.1:8000/api/posts/?ordering=title
    # http://127.0.0.1:8000/api/posts/?ordering=-title&search=first
    # http://127.0.0.1:8000/api/posts/?limit=5&offset=2

    # def get(self, request):
    #     post = Post.objects.all()
    #     serializer = PostSerializer(post, many=True)
    #     return Response(serializer.data)


class PostDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        post = Post.objects.filter(id=id).first()
        if not post:
            return Response({'status': 'fail', 'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response({'status': 'success', 'message': 'Post deleted'}, status=status.HTTP_200_OK)


class PostHandle(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'save post', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        id = request.GET.get('id')
        post = Post.objects.filter(id=id).first()
        if not post:
            return Response({'status': 'fail', 'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'status': 'success', 'message': 'get post', 'data': PostSerializer(post).data}, 200)

    def put(self, request):
        id = request.data.get('id')
        post = Post.objects.filter(id=id).first()
        if not post:
            return Response({'status': 'fail', 'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        if post.author.user != request.user:
            return Response({'status': 'fail', 'message': 'Only author can edit post'}, status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'Post updated', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': 'fail', 'message': 'Validation failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AuthorsHandle(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        id = request.GET.get('id')
        if id:
            author = Author.objects.filter(id=id).first()
            if author:
                serilizer = AuthorSerializer(author)
                return Response({'status': 'success', 'message': 'get author', 'data': serilizer.data}, status=status.HTTP_200_OK)

            return Response({'status': 'failed', 'message': f"no author {id}"}, status=status.HTTP_404_NOT_FOUND)
        authors = Author.objects.all()
        serilizer = AuthorSerializer(authors, many=True)
        return Response({'status': 'success', 'message': 'get all authors', 'data': serilizer.data}, status=status.HTTP_200_OK)

    # author create then register the user
    # def post(self, request):
    #     serializer = AuthorSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'message': 'author is created', 'data': serializer.data}, 200)
    #     return Response({'message': 'fail create aouthor', 'data': serializer.errors}, 400)

    def put(self, request):
        id = request.data.get('id')
        author = Author.objects.filter(id=id).first()
        if author:
            serializer = AuthorSerializer(author, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'success', 'message': 'author is upadated', 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response({'status': 'fail', 'message': 'no valid fields', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'fail', 'message': 'no author'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        id = request.data.get('id')
        author = Author.objects.filter(id=id).first()
        if author:
            author.delete()
            return Response({'status': 'success', 'message': 'author is deleted'}, status=status.HTTP_200_OK)
        return Response({'status': 'fail', 'message': 'no author'}, status=status.HTTP_404_NOT_FOUND)

# class AuthorsPosts(APIView):
#     def get(self, request):
#         id = request.GET.get('id')
#         if id:
#             author = Author.objects.filter(id = id).first()
#             if author:
#                 posts = Post.objects.filter(author = id)
#                 serializer = PostSerializer(posts, many=True)
#                 return Response({
#                     'message':f"all posts of auth {author.name}",
#                     'data': serializer.data
#                 }, 200)
#             return Response({'message':'author not found'}, 404)
#         return Response({'message':'id not found'}, 400)


class AuthorsPosts(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Get 'id' from query parameters
        author_id = request.GET.get('id')

        # If no 'id' is provided, return a 400 Bad Request
        if not author_id:
            return Response({'status': 'fail', 'message': 'Author ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Try to find the author by 'id'
        author = Author.objects.filter(id=author_id).first()

        if author:
            # Get all posts related to the found author
            posts = Post.objects.filter(author=author_id)
            serializer = PostSerializer(posts, many=True)

            # Return the serialized data for the author's posts
            return Response({
                'status': 'success',
                'message': f"All posts by author {author.name}",
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        # If the author does not exist, return a 404 Not Found
        return Response({'status': 'fail', 'message': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDetail(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        comment_id = request.GET.get('id')
        if comment_id:
            comment = Comment.objects.filter(id=comment_id).first()
            if comment:
                author = comment.author
                post = comment.post
                return Response({
                    'status': 'success',
                    'message': 'get comment detail',
                    'data': {
                        'author': AuthorSerializer(author).data,
                        'post': PostSerializer(post).data,
                        'comment': CommentSerializer(comment).data
                    }
                }, status=status.HTTP_200_OK)
            return Response(
                {
                    'status': 'fail',
                    'message': 'no comment found',
                }, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {
                'status': 'fail',
                'message': 'no comment id in request',
            }, status=status.HTTP_404_NOT_FOUND)
# class CommentDetail(APIView):
#     def get(self, request):
#         comment_id = request.GET.get('id')
#         if comment_id:
#             comment = Comment.objects.filter(id=comment_id).first()
#             if comment:
#                 # Serialize the comment, including nested data for Author and Post
#                 serializer = CommentSerializer(comment)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response({'message': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
#         return Response({'message': 'No ID provided'}, status=status.HTTP_400_BAD_REQUEST)


class Page(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # use build in authentification
        # if not request.user.is_authenticated:
        #     return Response({'message': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        post_id = request.GET.get('id')

        if post_id:
            # Retrieve the post by ID
            post = Post.objects.filter(id=post_id).first()

            if post:
                # Get all comments related to this post
                comments = post.comments.all()  # Correct way to access related comments
                return Response({
                    'status': 'success',
                    'message': 'Get page: post with comments',
                    'data': {
                        'post': PostSerializer(post).data,
                        'comments': CommentSerializer(comments, many=True).data
                    }
                }, status=status.HTTP_200_OK)

            return Response({'status': 'fail', 'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'status': 'fail', 'message': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)


class RootView(APIView):
    # throttle_classes = [AnonRateThrottle]
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            'status': 'success',
            'message': 'Welcome to the Django REST Framework API!',
            'endpoints': {
                '/api/': 'GET API root (available endpoints)',
                '/api/register/': 'POST Register new user',
                '/api/login/': 'POST Login (get JWT tokens)',

                '/api/posts/': 'GET Get all posts',
                '/api/posts/<int:id>/': 'DELETE Delete a specific post by ID',
                '/api/post/': 'POST Create a new post',
                '/api/post/': 'PUT Updatea a post',
                '/api/post/?id=<int>': 'GET Get post by ID',
                '/api/authors/': 'GET Get all authors',
                '/api/authors/': 'PUT Update author',
                '/api/authors/': 'DELETE Delete author',
                '/api/authors/?id=<int>': 'GET Get author by ID',

                '/api/authors/posts/?id=<int>': 'GET Get all posts by author ID',
                '/api/page/?id=<int>': 'GET Get post with comments by ID',

                '/api/comment/?id=<int>': 'GET Get detail about certain comment by ID',
                
                '/api/comments/': 'GET, POST, Handle comments (using viewset) get all comments, create new comment',
                '/api/comments/1/': 'GET, DELETE - comments by id, PUT, PATCH - update post',

                '/api/posts/?search=something': 'GET handle posts search',
                '/api/posts/?ordering=title': 'GET handle posts ordering',
                '/api/posts/?ordering=-title&search=first': 'GET handle posts reverse ordering and search',
                '/api/posts/?limit=5&offset=2': 'GET handle posts pagination, limit and offset',
            }
        })


class RegisterView(APIView):
    permission_classes = [AllowAny]  # Allow any user to register

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)  # Create the refresh token
            access = refresh.access_token  # Generate access token
            return Response({
                'status': 'success',
                'message': 'create new user',
                'data': {
                    'refresh': str(refresh),
                    'access': str(access),
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'fail',
            'message': 'fail to create new user',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# class CustomTokenObtainPairView(TokenObtainPairView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         return response
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Call the parent class to handle the normal token retrieval
        response = super().post(request, *args, **kwargs)

        # If the request was successful (status code 200), format the response
        if response.status_code == status.HTTP_200_OK:
            refresh = response.data.get('refresh')
            access = response.data.get('access')
            return Response({
                'status': 'success',
                'message': 'login successful',
                'data': {
                    'refresh': refresh,
                    'access': access,
                }
            }, status=status.HTTP_200_OK)

        # If there's an error (e.g., invalid credentials), return the default response
        return response
