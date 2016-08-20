from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, PhotoSerializer, CommentSerializer, LikeSerializer, DislikeSerializer
from .models import User, Photo, Comment, Like, Dislike, UserProfile
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.parsers import FileUploadParser
from django.contrib.auth import login, logout
from .auth import QuietBasicAuthentication
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.core.mail import send_mail
from django.utils import timezone
import hashlib, random, datetime


class AuthUser(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        return Response(UserSerializer(request.user, context={'request': request}).data)


class UserList(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()


class UserPhotoList(generics.ListAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]
    queryset = Photo.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user__username=self.kwargs.get('username')).order_by('-data')


class UserDetail(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAuthenticated]
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer)
    data = serializer_class.data
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
            self.object = self.get_object()
            following = request.user.following.all()
            isFollow = self.object in following
            return Response({'us': self.object, 'usercome': request.user, 'isFollow': isFollow}, template_name='profile.html')


class UserDetailForReturnJson(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()


class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [
        permissions.AllowAny
    ]
    queryset = Photo.objects.all()

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs.get('pk'))


class AllRandomPhotos(generics.ListAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]
    queryset = Photo.objects.order_by('?')[:20]


class LoginView(generics.CreateAPIView):
    authentication_classes = (QuietBasicAuthentication,)
    renderer_classes = (JSONRenderer,)

    def post(self, request, *args, **kwargs):
        login(request, request.user)
        return Response(UserSerializer(request.user, context={'request': request}).data)


class LogoutView(generics.DestroyAPIView):
    renderer_classes = (JSONRenderer,)

    def delete(self, request, *args, **kwargs):
            logout(request)
            return Response({})


class RegisterWithoutMail(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serialized = UserSerializer(data=request.DATA)
        if serialized.is_valid():
            User.objects.create_user(
                    serialized.initial_data['username'],
                    serialized.initial_data['email'],
                    serialized.initial_data['password'],
                    )
            return Response(status=200)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class Register(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serialized = UserSerializer(data=request.DATA)
        if serialized.is_valid():

            user = User.objects.create_user(
                    serialized.initial_data['username'],
                    serialized.initial_data['email'],
                    serialized.initial_data['password'],
                    )
            user.is_active = False
            user.save()

            username = serialized.initial_data['username']
            email = serialized.initial_data['email']

            salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
            activation_key = hashlib.sha1(str(salt).encode('utf-8')+str(email).encode('utf-8')).hexdigest()

            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            user = User.objects.get(username=username)

            new_profile = UserProfile(user=user, activation_key=activation_key, key_expires=key_expires)
            new_profile.save()
            email_subject = "Подтверждение регистрации на instagram-mephi.ru"
            email_body = "Привет %s, спасибо, что зарегистрировался на нашем сайте! Чтобы активировать свой аккаунт зайди" \
                         " по ссылке ниже, у тебя есть 48 часов! \
                                 http://127.0.0.1:8000/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'admin@instagram-mephi.ru', [email], fail_silently=False)
            return Response(status=status.HTTP_201_CREATED,)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


def register_confirm(request, activation_key):
    if request.user.is_authenticated():
        HttpResponseRedirect('/')
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    if user_profile.key_expires < timezone.now():
        return render_to_response('confirm_expired.html')

    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('confirm.html')


def register_success(request):
    if request.user.is_authenticated():
        return redirect('/users/'+request.user.username)
    else:
        return render_to_response('register_success.html')


def AuthView(request):
    if request.user.is_authenticated():
        return redirect('/users/'+request.user.username)
    else:
        return render_to_response('login.html')


def RegisterView(request):
    if request.user.is_authenticated():
        return redirect('/users/'+request.user.username)
    else:
        return render_to_response('register.html')


def IndexView(request):
    if request.user.is_authenticated():
        return redirect('/users/'+request.user.username)
    else:
        return render_to_response('index.html')


def SearchUsersView(request):
    if request.user.is_authenticated():
        return render_to_response('search.html')
    else:
        return render_to_response('login.html')


def AllPhotosView(request):
    if request.user.is_authenticated():
        return render_to_response('allphotos.html')
    else:
        return render_to_response('login.html')


class FeedView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        return Response({'auth__user': request.user}, template_name='feed.html')


class FollowersView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, username, *args, **kwargs):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        return Response({'auth__user': request.user, 'username': username}, template_name='followers.html')


class FollowingView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, username, *args, **kwargs):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        return Response({'auth__user': request.user, 'username': username}, template_name='following.html')


class FollowingList(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_queryset(self):
        return self.queryset.filter(followers__username=self.kwargs.get('username'))


class FollowersList(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_queryset(self):
        return self.queryset.filter(following__username=self.kwargs.get('username'))


class FeedPhotoList(generics.ListAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]
    queryset = Photo.objects.all()

    def get_queryset(self):
        start = int(self.kwargs.get('page'))*5
        end = start + 5
        return self.queryset.filter(user__in=User.objects.get(username=self.kwargs.get('username')).following.all()).order_by('-data')[start:end]


class AddFollowing(generics.UpdateAPIView):

    def put(self, request, username, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        fol = User.objects.get(username=username)
        user.following.add(fol)
        return Response({})


class AddPhoto(generics.CreateAPIView):
    permission_classes = [IsOwner]
    parser_classes = (FileUploadParser, )

    def post(self, request, user_id, *args, **kwargs):
        file_obj = request.data['file']
        if len(request.data['file']) > (10000*1024):
            return Response(status=400)
        else:
            upload = Photo(image=file_obj, user_id=user_id)
            upload.save()
            save_id = upload.id
            return Response(save_id, status=201)


class AddAvatar(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (FileUploadParser, )
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):

        file_obj = request.data['file']
        request.user.avatar = file_obj
        request.user.save()
        return Response(UserSerializer(request.user, context={'request': request}).data, status=200)


class AddComment(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    throttle_scope = 'comments'

    def post(self, request, image_id, user_id, *args, **kwargs):
        serialized = CommentSerializer(data=request.data, context={'request': request})
        photo = Photo.objects.get(id=image_id)
        if serialized.is_valid():
            serialized.save(image_id=image_id, user_id=user_id)
            photo.comment_count += 1
            photo.save()
            save_id = serialized.data
            return Response(save_id, status=status.HTTP_201_CREATED,)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class AddLike(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def post(self, request, image_id, state, *args, **kwargs):
        Photo.objects.get(id=image_id)
        try:
            like = Like.objects.get(username=request.user.username, image=image_id)
        except Like.DoesNotExist:
            like = None
        try:
            dislike = Dislike.objects.get(username=request.user.username, image=image_id)
        except Dislike.DoesNotExist:
            dislike = None
        if state == '0':
            if like is None and dislike is not None:
                arr = self.addOrDeleteLikeOrDislike(request, image_id, 2)
                dislike.delete()
                return Response(arr, status=201)
            elif like is None and dislike is None:
                arr = self.addOrDeleteLikeOrDislike(request, image_id, 3)
                return Response(arr, status=201)
            elif like is not None:
                arr = self.addOrDeleteLikeOrDislike(request, image_id, 1)
                like.delete()
                return Response(arr, status=201)
        else:
            if dislike is not None and like is None:
                arr = self.addOrDeleteLikeOrDislike(request, image_id, 4)
                dislike.delete()
                return Response(arr, status=201)
            elif dislike is None and like is not None:
                arr = self.addOrDeleteLikeOrDislike(request, image_id, 5)
                like.delete()
                return Response(arr, status=201)
            elif dislike is None and like is None:
                arr = self.addOrDeleteLikeOrDislike(request, image_id, 6)
                return Response(arr, status=201)

    def addOrDeleteLikeOrDislike(self, request, image_id, code):
        if code == 2 or code == 3:
            add_like = Like(username=request.user.username, image=image_id)
            add_like.save()
        elif code == 5 or code == 6:
            add_dislike = Dislike(username=request.user.username, image=image_id)
            add_dislike.save()
        photo = Photo.objects.get(id=image_id)
        if code == 1:
            photo.likes -= 1
        elif code == 2:
            photo.likes += 1
            photo.dislikes -= 1
        elif code == 3:
            photo.likes += 1
        elif code == 4:
            photo.dislikes -= 1
        elif code == 5:
            photo.dislikes += 1
            photo.likes -= 1
        elif code == 6:
            photo.dislikes += 1

        photo.save()
        arr = [photo.likes, photo.dislikes]
        return arr


class GetAllComments(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()

    def get_queryset(self):
        return self.queryset.filter(image_id=Photo.objects.filter(user__in=User.objects.get(username=self.kwargs.get('username')).following.all()).order_by('-data'))


class GetAllCommentsSinglePhoto(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()

    def get_queryset(self):
        return self.queryset.filter(image_id=self.kwargs.get('id')).order_by('data')


class GetNewPhoto(generics.RetrieveAPIView):
    lookup_field = 'pk'
    queryset = Photo.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoSerializer


class GetNewComment(generics.RetrieveAPIView):
    lookup_field = 'pk'
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()


class LikesUsername(generics.ListAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()

    def get_queryset(self):
        return self.queryset.filter(image=self.kwargs.get('image')).order_by('-id')


class DislikesUsername(generics.ListAPIView):
    serializer_class = DislikeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Dislike.objects.all()

    def get_queryset(self):
        return self.queryset.filter(image=self.kwargs.get('image')).order_by('-id')


class DeletePhoto(generics.DestroyAPIView):

    def delete(self, request, image_id, *args, **kwargs):
        queryset = Photo.objects.get(id=image_id)
        queryset.delete()
        queryset = Comment.objects.filter(image_id=image_id)
        queryset.delete()
        queryset = Like.objects.filter(image=image_id)
        queryset.delete()
        queryset = Dislike.objects.filter(image=image_id)
        queryset.delete()
        return Response({})


class DeleteFollowing(generics.DestroyAPIView):

    def delete(self, request, username, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        fol = User.objects.get(username=username)
        user.following.remove(fol)
        return Response({})


