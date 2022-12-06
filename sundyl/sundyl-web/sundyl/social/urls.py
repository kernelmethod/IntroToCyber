from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profiles/<int:user_id>", views.ProfileView.as_view(), name="profile"),
    path("profiles/followers/<int:user_id>", views.FollowerListView.as_view(), name="followers"),
    path("user/edit", views.ProfileEditView.as_view(), name="edit_profile"),
    path("user/upload", views.UserFileUpload.as_view(), name="upload_file"),
    path("user/follow/<int:user_id>", views.FollowUserView.as_view(), name="follow"),
]
