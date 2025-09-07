from django.shortcuts import redirect
from .models import *
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views import View
from .forms import *
from django.views.generic import DeleteView
from admins.views import islocked
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from taggit.models import Tag
from better_profanity import profanity
from django.core.exceptions import ValidationError


# ----------------------------------welcome function----------------------------------------
def welcome(request):
    return render(request, "core/welcome.html")


# ----------------------------------register function---------------------------------------
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # mobile_num = request.POST['mob']
        if request.POST['username'] == '' or request.POST['email'] == '' or request.POST['password'] == '' or \
                request.POST['password2'] == '':
            messages.info(request, 'Requierd Fields')
            return redirect('register')
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # ----log user in and redirect to settings page----
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # ----create a Profile object for the new user----
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('login')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('register')

        return redirect('login')
    else:
        return render(request, 'core/register.html')


# ------------------login function----------------------
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_staff:
                auth.login(request, user)
                return redirect('post')
            elif islocked(user):
                messages.info(request, "This Account is blocked , Please contact the admin ")
                return redirect('login')
            else:
                auth.login(request, user)
                return redirect("post")
        else:
            messages.info(request, 'Invalid information')
            return redirect('login')

    else:
        return render(request, 'core/login.html')


# ---------------------------logout function------------------------
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')


# ---------------------------show the blog page--------------------
@login_required(login_url='login')
def show(request):
    return render(request, 'core/show.html')


# --------------------------Edit profile function-------------------
@login_required(login_url='login')
def editprofile(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') is None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        if request.FILES.get('image') is not None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('editprofile')
    return render(request, 'core/editprofile.html', {'user_profile': user_profile})


# ---------------------------Posts  in main page--------------------------
def post(request):
    posts = Post.objects.order_by('-created_at')
    categories = Category.get_all_categories()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    tags = Tag.objects.all()
    context = {"posts": posts, "categories": categories, 'page_obj': page_obj, 'tags': tags}
    return render(request, "core/show.html", context)


# ----------------------------Posts in category-----------------------------
def createpost(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST.get('title')
            content = request.POST.get('content')

        postform = form.save(commit=False)
        #  ----If the content contains forbidden words----

        bad_words = ['']
        words = ForbiddenWords.objects.all()
        for word in words:
            bad_words.append(str(word.forbidden_word))

        profanity.add_censor_words(bad_words)
        postform.content = profanity.censor(content)
        #  ----If the title contains forbidden words----

        bad_words = ['']
        words = ForbiddenWords.objects.all()
        for word in words:
            bad_words.append(str(word.forbidden_word))

        profanity.add_censor_words(bad_words)
        postform.title = profanity.censor(title)
        postform.user = request.user
        postform.save()
        form.save_m2m()
        return HttpResponseRedirect(Post.get_all_url())

    context = {'post': form}
    return render(request, 'core/create.html', context)


# ---------------------------------show post's category------------------------------
def catPosts(request, cat_id):
    cat_post = Post.objects.filter(category_id=cat_id).order_by('-created_at')

    context = {'cat_post': cat_post}
    return render(request, 'core/cat-posts.html', context)


# -------------------------------------tags function----------------------------------
def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # ---Filter posts by tag name---

    posts = Post.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'posts': posts,
    }
    return render(request, 'core/tag-posts.html', context)


# ---------------------------------categories subscribe------------------------------
def subscribe(request, cat_id):
    user = request.user
    category = Category.objects.get(id=cat_id)
    category.user.add(user)
    # ----sending email to the user----
    try:
        send_mail("subscribed to a new category",
                  'hello ,\nyou have just subscribed to category ' + category.cat_name,
                  settings.EMAIL_HOST_USER,
                  [request.user.email],
                  fail_silently=False)
    except Exception as ex:
        raise ValidationError("Couldn't send the message to the email ! " + str(ex))
    return redirect("post")


# ---------------------------------categories unsubscribe-------------------------------
def unsubscribe(request, cat_id):
    user = request.user
    category = Category.objects.get(id=cat_id)
    category.user.remove(user)
    return redirect("post")


# --------------------------------------Post details------------------------------------
class PostDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        return render(request, 'core/details.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            #  ----If the comment contains forbidden words-----

            bad_words = ['']
            words = ForbiddenWords.objects.all()
            for word in words:
                bad_words.append(str(word.forbidden_word))

            profanity.add_censor_words(bad_words)
            new_comment.content = profanity.censor(new_comment.content)
            new_comment.save()
            form = CommentForm()

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'core/details.html', context)


# -----------------------------------------Like post----------------------------------
class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        if not is_like:
            post.likes.add(request.user)
        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


# ----------------------------------------Dislike post------------------------------------
class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        if is_like:
            post.likes.remove(request.user)

        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if not is_dislike:
            post.dislikes.add(request.user)
            # -----Delete post if dislike = 10------
            if post.dislikes.all().count() == 6:
                post.delete()

                return redirect('post')
        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


# ------------------------------------------Edit post----------------------------------------
def editpost(request, post_id):
    post = Post.objects.get(id=post_id)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            title = request.POST.get('title')
            content = request.POST.get('content')

        postform = form.save(commit=False)
        #  ----If the content contains forbidden words-----

        bad_words = ['']
        words = ForbiddenWords.objects.all()
        for word in words:
            bad_words.append(str(word.forbidden_word))

        profanity.add_censor_words(bad_words)
        postform.content = profanity.censor(content)
        #  If the title contains forbidden words
        bad_words = ['']
        words = ForbiddenWords.objects.all()
        for word in words:
            bad_words.append(str(word.forbidden_word))

        profanity.add_censor_words(bad_words)
        postform.title = profanity.censor(title)
        postform.user = request.user
        postform.save()
        form.save_m2m()
        return HttpResponseRedirect(Post.get_all_url())

    context = {'post': form}
    return render(request, 'core/editpost.html', context)


# ---------------------------------------delete post----------------------------------
class PostDelete(DeleteView):
    model = Post
    template_name = "core/delete.html"
    success_url = '/posts'


# --------------------------------------comment like----------------------------------
class AddCommentLike(View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_dislike = False
        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like = False
        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break
        if not is_like:
            comment.likes.add(request.user)
        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


# -----------------------------------------comment dislike--------------------------------
class AddCommentDislike(View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)
        is_like = False
        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break
        if is_like:
            comment.likes.remove(request.user)

        is_dislike = False
        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if not is_dislike:
            comment.dislikes.add(request.user)
        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


# -----------------------------------------comment replay----------------------------------
class CommentReplyView(View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.parent = parent_comment

            #  ---If the replay contains forbidden words---
            bad_words = ['']
            words = ForbiddenWords.objects.all()
            for word in words:
                bad_words.append(str(word.forbidden_word))

            profanity.add_censor_words(bad_words)
            new_comment.content = profanity.censor(new_comment.content)
            new_comment.save()

        return redirect('details', pk=post_pk)


# --------------------------------------------comment delete--------------------------------
class CommentDeleteView(DeleteView):
    model = Comment
    template_name = "core/comment_delete.html"
    success_url = '/posts'


# -----------------------------------search by post title and tags --------------------------
def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        try:
            tag = Tag.objects.get(slug=searched)
            posts = Post.objects.filter(tags=tag)
        except:
            posts = Post.objects.filter(title=searched)

        context = {'searched': searched, 'posts': posts}

        return render(request, 'core/search.html', context)
    else:
        return render(request, 'core/search.html', {})
