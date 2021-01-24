from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (TemplateView, ListView, DetailView, CreateView,
                                    UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.utils import timezone
# Create your views here.
##################################################################################
#POST VIEWS!!!#
#About page
class About(TemplateView):
    template_name = 'blog/about.html'

#displaying the list of post on home page so in urls.py(project) will be mapped as home page
class PostListView(ListView):
    model = Post
    context_object_name='post_list'
     #to show only those post that has been published(i.e. published_date is !null)
    def get_queryset(self):
         #this is a sql query like linq in .net
         return Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
                #select * from Post where published_date <= NOW() orderby published_date

#displaying details of particular post
class PostDetailView(DetailView):
     model = Post

#create the post but grant access to those only those are the user(here superuser)
#LoginRequiredMixin acts same as the decorators, it checks wether loggedin or not
class PostCreateView(LoginRequiredMixin,CreateView):
     login_url='/login/'#Default return value for function get_login_url()
     #get_login_url()
     #Returns the URL that users who don’t pass the test(are not loggedin)
     # will be redirected to. Returns login_url if set, or settings.LOGIN_URL otherwise.

     redirect_field_name = 'blog/post_detail.html'#Default return value for function get_redirect_field_name().
     #get_redirect_field_name()
     #Returns the name of the query parameter that will contain the URL
     #the user should be redirected to after a successful login

     form_class = PostForm #connects forms.py to model.py
     model = Post

#update the post i.e. lets you edit the post
#same as create, only user(here superuser) can edit the post
class PostUpdateView(LoginRequiredMixin, UpdateView):
     login_url = '/login/'
     redirect_field_name = 'blog/post_detail.html'
     form_class = PostForm #connects forms.py to model.py
     model = Post

#Deletes the form
#same as create, only user(here superuser) can edit the post
class PostDeleteView(LoginRequiredMixin,DeleteView):

    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    model = Post
    success_url = reverse_lazy('blog:post_list')

#display list of posts which are draft i.e. dont have any published_date
class DraftView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post
    context_object_name = 'posts'
    #sql query where published_date is null
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

#function for publishing the posts
#but to publish we need to be loggedin, hence for function we use decorators
@login_required
def post_publish(request, pk):
     post = get_object_or_404(Post, pk=pk) #creates object post with particular pk
     post.publish()
     return redirect('blog:post_detail',pk=pk) #have to specify the pk as in url it require it as parameter


######################################################################################################
#COMMENT VIEWS!!!!!#

#funtion for comment form which add comments to the post
#for that user need to be loggedin
@login_required
def add_comment_to_post(request, pk):
     post = get_object_or_404(Post, pk=pk)
     if request.method == 'POST':
         form = CommentForm(request.POST)
         if form.is_valid():
             comment = form.save(commit=False)
             comment.post = post #Comment model there is a post which is a fk,
             #this statement is assigning this->post object to the table->post and hence filling all entities in Table
             comment.save()
             return redirect('blog:post_detail', pk=post.pk)
     else:#ie a get request
        form=CommentForm()
        return render(request,'blog/comment_form.html', {'form':form})

#function for approving the comment, hence loggedin require
@login_required
def comment_approve(request,pk):
     comment = get_object_or_404(Comment, pk=pk)
     comment.approve() #Comment model we created the method approve
     return redirect('blog:post_detail', pk=comment.post.pk)

#funtion for deletion
@login_required
def comment_remove(request, pk):
     comment = get_object_or_404(Comment, pk=pk)
     post_pk = comment.post.pk
     comment.delete() #just like .save(), delete() method is builtin to django
     return redirect('blog:post_draft_list')
