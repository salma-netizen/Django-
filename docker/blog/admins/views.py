from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required
from core.models import Profile
from core.models import *
from core.forms import *
from better_profanity import profanity
from django.http import HttpResponseRedirect


# ---------------------function to allow the admins to login in admin admin panel---------------------
def loginAdmin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_staff:
                auth.login(request, user)
                return redirect('interface')
            else:
                messages.info(request, "This Account is not a staff ")
                return redirect('admin')
        else:
            messages.info(request, 'Invalid information')
            return redirect('admin')

    else:
        return render(request, 'admins/loginadmin.html')


# -----------------------function to allow the admins to logout from the admin panel------------------
def logoutAdmin(request):
    logout(request)
    return redirect("admin")


# ----------------------------the interface page for the admin page-----------------------------------
@staff_member_required(login_url="admin")
def interface(request):
    # get all normal users
    users = User.objects.filter(is_staff=False)
    context = {'users': users}
    return render(request, 'admins/interface.html', context)


# ----------------------------view to promote the user to an admin---------------------------------------
def promoteUser(request, id):
    user = User.objects.get(id=id)
    # check if the user is not blocked he can be promoted
    # and that's by making the is_staff attribute and is_superuser equal true
    if not islocked(user):
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return redirect('interface')
    else:
        return redirect('interface')


# -------------------------------------show all the admins-------------------------------------------
@staff_member_required(login_url="admin")
def showAdmins(request):
    admins = User.objects.filter(is_staff=True, is_superuser=True)
    context = {'admins': admins}
    return render(request, 'admins/admins.html', context)


# --------------lock the required account first then lock the user associated to that account------------
@staff_member_required(login_url="admin")
def lockUser(request, id):
    user = User.objects.get(id=id)
    lock_user(user)
    return redirect('interface')


def lock_user(user):
    account = Profile.objects.get(user=user)
    account.is_locked = True
    account.save()


# -------------unlock the required account first then unlock the user associated to that account--------
@staff_member_required(login_url="admin")
def unlockUser(request, id):
    user = User.objects.get(id=id)
    unlock_user(user)
    return redirect('interface')


def unlock_user(user):
    account = Profile.objects.get(user=user)
    account.is_locked = False
    account.save()


# ---------------function to return the status of the account if it is locked or not--------------------
def islocked(user):
    return Profile.objects.get(user=user).is_locked


# ------------------------------add the forbidden words in admin page------------------------------------
@staff_member_required(login_url="admin")
def addForbidden(request):
    form = ForbiddenWordsForm()
    if request.method == 'POST':
        form = ForbiddenWordsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("forbiddenwords")
    context = {"word_form": form}
    return render(request, "admins/forbiddenwordform.html", context)


# --------------------------------------show all the forbidden words-------------------------------------
@staff_member_required(login_url="admin")
def showForbidden(request):
    forbidden_words = ForbiddenWords.objects.all()
    context = {'forbidden_words': forbidden_words}
    return render(request, "admins/forbiddenwords.html", context)


# -------------------------------delete specific forbidden word using the word id-------------------------
@staff_member_required(login_url="admin")
def delForbidden(request, word_id):
    forbidden_words = ForbiddenWords.objects.get(id=word_id)
    forbidden_words.delete()
    return redirect('forbiddenwords')


# -------------------------------Edit specific forbidden word using the word id--------------------------
@staff_member_required(login_url="admin")
def editForbidden(request, word_id):
    forbidden_words = ForbiddenWords.objects.get(id=word_id)
    form = ForbiddenWordsForm(instance=forbidden_words)
    if request.method == 'POST':
        form = ForbiddenWordsForm(request.POST, instance=forbidden_words)
        if form.is_valid():
            form.save()
            return redirect('forbiddenwords')
    context = {"word_form": form}
    return render(request, "admins/editforbiddenwords.html", context)


# --------------------------------------------Add Post by admin------------------------------------------
@staff_member_required(login_url="admin")
def addPost(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST.get('title')
            content = request.POST.get('content')

        postform = form.save(commit=False)
        #  If the content contains forbidden words

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

    context = {'form': form}
    return render(request, 'admins/postform.html', context)


# --------------------------------------------Edit Post by admin------------------------------------------
@staff_member_required(login_url="admin")
def editpost(request, post_id):
    post = Post.objects.get(id=post_id)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            title = request.POST.get('title')
            content = request.POST.get('content')

        postform = form.save(commit=False)
        #  If the content contains forbidden words

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

    context = {'form': form}
    return render(request, 'admins/editpost.html', context)


# ---------------------------------------Delete post by admin-----------------------------------
@staff_member_required(login_url="admin")
def deletePost(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect("posts")


# ----------------------------------------show posts-------------------------------------------
@staff_member_required(login_url="admin")
def showPosts(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'admins/posts.html', context)


# _________________________________show category__________________________________________
@staff_member_required(login_url="admin")
def showCategory(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'admins/categories.html', context)


# ---------------------------------add category--------------------------------------------------
@staff_member_required(login_url="admin")
def addCategory(request):
    # ----create category form-----
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # -----checking the form if it's valid or not-----
        if form.is_valid():
            form.save()
            return redirect("category")
    context = {"cat_form": form}
    return render(request, "admins/categoryform.html", context)


# ----------------------------------delete category-------------------------------------------
@staff_member_required(login_url="admin")
def deleteCategory(request, cat_id):
    category = Category.objects.get(id=cat_id)
    category.delete()
    return redirect("category")


# --------------------------------edit category----------------------------------------------
@staff_member_required(login_url="admin")
def editCategory(request, cat_id):
    category = Category.objects.get(id=cat_id)
    # put the category object which we want to edit into the form method by assigning it to the instance attribute
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category')
    context = {"cat_form": form}
    return render(request, "admins/editcategory.html", context)
