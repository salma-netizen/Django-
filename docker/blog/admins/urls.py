from django.urls import path
from admins import views


urlpatterns = [
    path('', views.loginAdmin, name="admin"),
    path('logoutadmin', views.logoutAdmin, name="logoutadmin"),
    path('interface/', views.interface, name='interface'),
    path('admins/', views.showAdmins, name='admins'),
    path('promote/<id>', views.promoteUser, name="promote"),
    path('lock/<int:id>', views.lockUser, name="lock"),
    path('unlock/<id>', views.unlockUser, name="unlock"),
    path('forbiddenwords/', views.showForbidden, name="forbiddenwords"),
    path('forbiddenwordform/', views.addForbidden, name="addforbiddenwords"),
    path('delforbidden/<word_id>', views.delForbidden, name="delforbiddenwords"),
    path('editforbidden/<word_id>', views.editForbidden, name="editforbiddenwords"),
    path('posts/', views.showPosts, name="posts"),
    path('postform/', views.addPost, name="addpost"),
    path('deletepost/<post_id>', views.deletePost, name="deleteposts"),
    path('editpost/<post_id>', views.editpost, name="editposts"),
    path('categories/', views.showCategory, name="category"),
    path('categoryform/', views.addCategory, name="addcategory"),
    path('deletecat/<cat_id>', views.deleteCategory, name="deletecat"),
    path('editcat/<cat_id>', views.editCategory, name="editcat"),
]