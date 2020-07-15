from django.shortcuts import render, get_object_or_404, redirect
from .models import tweet,Preference,Comment
from network.models import Follow, profile
import sys
from .forms import NewCommentForm
from django.contrib.auth.models import User
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.db.models import Count
from django.contrib.auth.decorators import login_required

# Create your views here.

def is_users(post_user, logged_user):
    return post_user == logged_user


PAGINATION_COUNT = 4

class FollowsListView(ListView):
    model = Follow
    template_name = 'feed/follow.html'
    context_object_name = 'follows'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.visible_user()
        return Follow.objects.filter(user=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['follow'] = 'follows'
        return data


class FollowersListView(ListView):
    model = Follow
    template_name = 'feed/follow.html'
    context_object_name = 'follows'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.visible_user()
        return Follow.objects.filter(follow_user=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['follow'] = 'followers'
        return data


class UserPostListView(LoginRequiredMixin, ListView):
    model = tweet
    template_name = 'feed/user_posts.html'
    context_object_name = 'posts'
    paginate_by = PAGINATION_COUNT

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        visible_user = self.visible_user()
        logged_user = self.request.user
        print(logged_user.username == '', file=sys.stderr)

        if logged_user.username == '' or logged_user is None:
            can_follow = False
        else:
            can_follow = (Follow.objects.filter(user=logged_user,
                                                follow_user=visible_user).count() == 0)
        data = super().get_context_data(**kwargs)

        data['user_profile'] = visible_user
        data['can_follow'] = can_follow
        return data

    def get_queryset(self):
        user = self.visible_user()
        return tweet.objects.filter(uname=user).order_by('-datetime')

    def post(self, request, *args, **kwargs):
        if request.user.id is not None:
            follows_between = Follow.objects.filter(user=request.user,
                                                    follow_user=self.visible_user())

            if 'follow' in request.POST:
                    new_relation = Follow(user=request.user, follow_user=self.visible_user())
                    if follows_between.count() == 0:
                        new_relation.save()
            elif 'unfollow' in request.POST:
                    if follows_between.count() > 0:
                        follows_between.delete()

        return self.get(self, request, *args, **kwargs)

class AllListView(LoginRequiredMixin,ListView):
    model=tweet
    template_name='feed/following.html'
    order_by=['-datetime']
    paginate_by = PAGINATION_COUNT

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        all_users = []
        data_counter = tweet.objects.values('uname')\
            .annotate(uname_count=Count('uname'))\
            .order_by('-uname_count')[:6]

        for aux in data_counter:
            all_users.append(User.objects.filter(pk=aux['uname']).first())
        # if Preference.objects.get(user = self.request.user):
        #     data['preference'] = True
        # else:
        #     data['preference'] = False
        data['preference'] = Preference.objects.all()
        # print(Preference.objects.get(user= self.request.user))
        data['all_users'] = all_users
        print(all_users, file=sys.stderr)
        return data

    def get_queryset(self):
        
        return tweet.objects.all().order_by('-datetime')


class TweetListView(LoginRequiredMixin,ListView):
    model=tweet
    template_name='feed/home.html'
    order_by=['-datetime']
    paginate_by = PAGINATION_COUNT

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        all_users = []
        data_counter = tweet.objects.values('uname')\
            .annotate(uname_count=Count('uname'))\
            .order_by('-uname_count')[:6]

        for aux in data_counter:
            all_users.append(User.objects.filter(pk=aux['uname']).first())
        # if Preference.objects.get(user = self.request.user):
        #     data['preference'] = True
        # else:
        #     data['preference'] = False
        data['preference'] = Preference.objects.all()
        # print(Preference.objects.get(user= self.request.user))
        data['all_users'] = all_users
        print(all_users, file=sys.stderr)
        return data

    def get_queryset(self):
        user = self.request.user
        qs = Follow.objects.filter(user=user)
        follows = [user]
        for obj in qs:
            follows.append(obj.follow_user)
        return tweet.objects.filter(uname__in=follows).order_by('-datetime')

class PostDetailView(DetailView):
    model = tweet
    template_name = 'feed/tweetdetail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments_connected = Comment.objects.filter(post_connected=self.get_object()).order_by('-date_posted')
        data['comments'] = comments_connected
        data['form'] = NewCommentForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(content=request.POST.get('content'),
                              author=self.request.user,
                              post_connected=self.get_object())
        new_comment.save()

        return self.get(self, request, *args, **kwargs)
   

class TweetCreateView(LoginRequiredMixin,CreateView):
     model=tweet
     
     fields=['text']
     success_url='/'
     
     def form_valid(self,form):
         form.instance.uname=self.request.user
         return super().form_valid(form)
         
class TweetUpdateView(LoginRequiredMixin,UpdateView):
     model=tweet
     
     fields=['text']
     success_url='/'
     
     def form_valid(self,form):
         form.instance.uname=self.request.user
         return super().form_valid(form)
         
     def test_func(self):
        tweet=self.get_object()
        if(self.request.user==tweet.uname):
            return True
        return False

class TweetDeleteView(LoginRequiredMixin,DeleteView):
     model=tweet
     
     
     success_url='/'
         
     def test_func(self):
        tweet=self.get_object()
        if(self.request.user==tweet.uname):
            return True
        return False

# Like Functionality====================================================================================
@login_required
def postpreference(request, tweetid, userpreference):
        if request.method == "POST":
                eachtweet= get_object_or_404(tweet, id=tweetid)
                obj=''
                valueobj=''
                try:
                        obj= Preference.objects.get(user= request.user, tweet= eachtweet)
                        valueobj= obj.value 
                        valueobj= int(valueobj)
                        userpreference= int(userpreference)
                        if valueobj != userpreference:
                                obj.delete()
                                upref= Preference()
                                upref.user= request.user
                                upref.tweet= eachtweet
                                upref.value= userpreference
                                if userpreference == 1 and valueobj != 1:
                                        eachtweet.likes += 1
                                        eachtweet.dislikes -=1
                                elif userpreference == 2 and valueobj != 2:
                                        eachtweet.dislikes += 1
                                        eachtweet.likes -= 1
                                upref.save()
                                eachtweet.save()
                                context= {'eachtweet': eachtweet,
                                  'tweetid': tweetid}
                                return redirect('home')
                        elif valueobj == userpreference:
                                obj.delete()
                                if userpreference == 1:
                                        eachtweet.likes -= 1
                                elif userpreference == 2:
                                        eachtweet.dislikes -= 1
                                eachtweet.save()
                                context= {'eachtweet': eachtweet,
                                  'tweetid': tweetid}
                                return redirect('home')
                                
                except Preference.DoesNotExist:
                        upref= Preference()
                        upref.user= request.user
                        upref.tweet= eachtweet
                        upref.value= userpreference
                        userpreference= int(userpreference)
                        if userpreference == 1:
                                eachtweet.likes += 1
                        elif userpreference == 2:
                                eachtweet.dislikes +=1
                        upref.save()
                        eachtweet.save()                            

                        context= {'eachtweet': eachtweet,
                          'tweetid': tweetid}

                        return redirect('home')

        else:
                eachtweet= get_object_or_404(tweet, id=tweetid)
                context= {'eachtweet': eachtweet,
                          'tweetid': tweetid}

                return redirect('home')