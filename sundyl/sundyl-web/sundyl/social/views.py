from django import http
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.shortcuts import redirect, render
from django.views.generic import View
from sundyl import settings
from sundyl.login.mixins import LoginRequiredMixin
from .forms import UserProfileForm, UserUploadForm
from .models import UserProfile, UserUpload, UserFollowing


def index(request):
    if request.user.is_authenticated:
        print(f"{request.user = }")

    return render(request, "index.html")


class ProfileView(View):
    def get(self, request, *args, **kwargs):
        if (user_id := kwargs.get("user_id")) is None:
            return http.HttpResponseBadRequest("No user ID was supplied")

        try:
            profile = UserProfile.objects.filter(user__id=user_id).get()
        except UserProfile.DoesNotExist:
            raise http.Http404("User profile not found")

        # Get relationship between logged-in user and this user
        if request.user.is_authenticated:
            try:
                rel = UserFollowing.objects.filter(source_user=request.user.profile).get()
                is_following = True
            except UserFollowing.DoesNotExist:
                is_following = False
        else:
            is_following = False

        # Check whether this user has completed the XSS challenge
        if not profile.successful_xss:
            followers = profile.followers
            try:
                followers.filter(source_user__user__username="freddy_obrzut").get()

                # Support user was among user's followers; user successfully completed
                # the XSS challenge!
                profile.successful_xss = True
                profile.save()

            except UserFollowing.DoesNotExist:
                # XSS challenge has not been completed
                pass

        files = UserUpload.objects.filter(user__id=user_id, public=True)
        context = {
            "profile": profile,
            "uploaded_files": files,
            "is_following": is_following,
            "csrf_flag": settings.FLAG_CSRF,
            "xss_flag": settings.FLAG_XSS,
        }

        # Check if the support user is following this user
        return render(request, "profile.html", context)


class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = UserProfile.objects.filter(user__id=request.user.id).get()
        form = UserProfileForm(instance=profile)

        context = {
            "form": form,
            "profile": profile,
        }

        return render(request, "edit_profile.html", context)

    def post(self, request, *args, **kwargs):
        # Update user's profile
        profile = request.user.profile
        form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if not form.is_valid():
            profile = UserProfile.objects.filter(user__id=request.user.id).get()
            context = {
                "form": form,
                "profile": profile,
            }
            return render(request, "edit_profile.html", context, status=422)

        form.save()
        return redirect("profile", request.user.id)


class UserFileUpload(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = UserUploadForm()
        return render(request, "upload.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserUploadForm(request.POST, request.FILES)

        if not form.is_valid():
            return render(request, "upload.html", {"form": form}, status=422)

        upload = form.cleaned_data["upload"]
        file = UserUpload(user=request.user, upload=upload, public=form.cleaned_data["public"])
        file.save()

        return render(request, "upload_success.html", {"upload": file})


class FollowUserView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if (user_id := kwargs.get("user_id")) is None:
            return http.HttpResponse("No user ID was supplied", status=400)

        if user_id == request.user.id:
            return http.HttpResponse("You cannot follow or unfollow yourself", status=422)

        dest_user = UserProfile.objects.filter(user__id=user_id).get()

        try:
            relationship = UserFollowing.objects.filter(source_user=request.user.profile).get()
            relationship.delete()
        except UserFollowing.DoesNotExist:
            # User is not currently following the target, so we should create a new
            # relationship between them
            UserFollowing(source_user=request.user.profile, dest_user=dest_user).save()

        return redirect("profile", user_id)


class FollowerListView(LoginRequiredMixin, View):
    """View that displays the followers of a given user."""

    def get(self, request, *args, **kwargs):
        if (user_id := kwargs.get("user_id")) is None:
            return http.HttpResponse("No user ID was supplied", status=400)

        profile = UserProfile.objects.filter(user__id=user_id).get()
        followers = list(profile.followers.all())

        # Get relationship between logged-in user and this user
        if request.user.is_authenticated:
            try:
                rel = UserFollowing.objects.filter(
                    source_user=request.user.profile,
                    dest_user=profile,
                ).get()
                is_following = True
            except UserFollowing.DoesNotExist:
                is_following = False
        else:
            is_following = False

        context = {
            "profile": profile,
            "followers": followers,
            "is_following": True,
        }
        return render(request, "followers.html", context)
