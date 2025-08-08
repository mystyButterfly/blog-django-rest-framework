from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostList, PostDelete, PostHandle, AuthorsHandle, AuthorsPosts, CommentViewSet, CommentDetail, Page, RootView, RegisterView, CustomTokenObtainPairView
router = DefaultRouter()
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('posts/', PostList.as_view(), name='post-list'),
    path('posts/<int:id>/', PostDelete.as_view(), name='post-delete'),
    path('post/', PostHandle.as_view(), name='post-list'),
    path('authors/', AuthorsHandle.as_view(), name='authors'),
    path('authors/posts/', AuthorsPosts.as_view(), name='authors.posts'),
    path('comment/', CommentDetail.as_view()),
    path('page/', Page.as_view()),
    path('', RootView.as_view(), name='root-api'),
    path('', include(router.urls)),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),

]
