from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from accounts.models import User
from baseapp.models import Blog, Category, Comment, Like
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class StaffRequiredMixin(UserPassesTestMixin):
    """Mixin to ensure only staff users can access admin views"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff
    
    def handle_no_permission(self):
        from django.shortcuts import redirect
        from django.contrib import messages
        messages.error(self.request, 'You do not have permission to access the admin dashboard.')
        return redirect('index')


class AdminDashboardView(StaffRequiredMixin, TemplateView):
    """Main admin dashboard with statistics"""
    template_name = 'admin_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get statistics
        context['total_users'] = User.objects.count()
        context['total_blogs'] = Blog.objects.count()
        context['total_comments'] = Comment.objects.count()
        context['total_categories'] = Category.objects.count()
        context['total_likes'] = Like.objects.count()
        
        # Recent activity
        context['recent_blogs'] = Blog.objects.select_related('author', 'category').order_by('-created_at')[:5]
        context['recent_comments'] = Comment.objects.select_related('user', 'blog').order_by('-created_at')[:5]
        context['recent_users'] = User.objects.order_by('-date_joined')[:5]
        
        # Top categories by blog count
        context['top_categories'] = Category.objects.annotate(
            blog_count=Count('blogs')
        ).order_by('-blog_count')[:5]
        
        return context


class AdminUserListView(StaffRequiredMixin, ListView):
    """User management interface"""
    model = User
    template_name = 'admin_users.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = User.objects.annotate(
            blog_count=Count('blogs'),
            comment_count=Count('comments')
        ).order_by('-date_joined')
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(name__icontains=search_query)
            )
        
        # Filter by status
        status_filter = self.request.GET.get('status', '')
        if status_filter == 'active':
            queryset = queryset.filter(is_active=True)
        elif status_filter == 'inactive':
            queryset = queryset.filter(is_active=False)
        elif status_filter == 'staff':
            queryset = queryset.filter(is_staff=True)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['status_filter'] = self.request.GET.get('status', '')
        return context


class AdminBlogListView(StaffRequiredMixin, ListView):
    """Blog management interface"""
    model = Blog
    template_name = 'admin_blogs.html'
    context_object_name = 'blogs'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Blog.objects.select_related('author', 'category').annotate(
            comment_count=Count('comments'),
            like_count=Count('likes')
        ).order_by('-created_at')
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(author__username__icontains=search_query)
            )
        
        # Filter by category
        category_filter = self.request.GET.get('category', '')
        if category_filter:
            queryset = queryset.filter(category__slug=category_filter)
        
        # Filter by author
        author_filter = self.request.GET.get('author', '')
        if author_filter:
            queryset = queryset.filter(author__username=author_filter)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['category_filter'] = self.request.GET.get('category', '')
        context['author_filter'] = self.request.GET.get('author', '')
        context['categories'] = Category.objects.all()
        context['authors'] = User.objects.filter(blogs__isnull=False).distinct()
        return context


class AdminCategoryListView(StaffRequiredMixin, ListView):
    """Category management interface"""
    model = Category
    template_name = 'admin_categories.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.annotate(
            blog_count=Count('blogs')
        ).order_by('name')


class AdminCommentListView(StaffRequiredMixin, ListView):
    """Comment moderation interface"""
    model = Comment
    template_name = 'admin_comments.html'
    context_object_name = 'comments'
    paginate_by = 30
    
    def get_queryset(self):
        queryset = Comment.objects.select_related('user', 'blog').order_by('-created_at')
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(message__icontains=search_query) |
                Q(user__username__icontains=search_query) |
                Q(blog__title__icontains=search_query)
            )
        
        # Filter by blog
        blog_filter = self.request.GET.get('blog', '')
        if blog_filter:
            queryset = queryset.filter(blog__slug=blog_filter)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['blog_filter'] = self.request.GET.get('blog', '')
        context['blogs'] = Blog.objects.all()
        return context
