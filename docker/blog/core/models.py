from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.shortcuts import reverse
from taggit.managers import TaggableManager

User = get_user_model()


# ---------------------------------profile class----------------------------------------
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_profileimg_url(self):
        return f"/media/{self.profileimg}"


# ---------------------------------category class-------------------------------------------
class Category(models.Model):
    cat_name = models.CharField(max_length=100)
    user = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.cat_name

    @classmethod
    def get_all_categories(cls):
        return cls.objects.all()

    @classmethod
    def get_category(cls, id):
        return get_object_or_404(cls, pk=id)


# ----------------------------------Post class---------------------------------------------
class Post(models.Model):
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    picture = models.ImageField(null=True, upload_to='posts/images/')
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    @classmethod
    def get_all_posts(cls):
        return cls.objects.all()

    @classmethod
    def show_post(cls, id):
        return get_object_or_404(cls, pk=id)

    def get_picture_url(self):
        return f"/media/{self.picture}"

    def get_edit_url(self):
        return reverse("editpost", args=[self.id])

    def get_post_url(self):
        return reverse("details", args={self.id})

    def get_delete_url(self):
        return reverse("deletepost", args={self.id})

    @classmethod
    def get_all_url(cls):
        return reverse("post")


# ---------------------------------------Comment class-----------------------------------
class Comment(models.Model):
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')

    def __str__(self):
        return self.user.username

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created_on').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    def get_deletecomment_url(self):
        return reverse("deletecomment", args={self.id})


# ----------------------------------------ForbiddenWords class-----------------------------
class ForbiddenWords(models.Model):
    forbidden_word = models.CharField(max_length=100)

    def __str__(self):
        return self.forbidden_word
