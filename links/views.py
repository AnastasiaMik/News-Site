# -*- coding: utf-8 -*-
from django.http import HttpResponse
from .models import Link, Vote, UserProfile
from django.views.generic import ListView, DetailView
from django.contrib.auth import get_user_model
from django.views.generic.edit import UpdateView
from .forms import UserProfileForm, LinkForm, VoteForm
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView, FormView


class UserProfileEditView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "edit_profile.html"

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("profile", kwargs={'slug': self.request.user})

class LinkListView(ListView):
    model = Link
    queryset = Link.with_votes.all()
    paginate_by = 3 #количество новостей на странице

class LinkDetailView(DetailView):
    model = Link

class LinkCreateView(CreateView):
    model = Link
    form_class = LinkForm

    def form_valid(self, form):
        f = form.save(commit=False)
        f.rank_score = 0.0
        f.submitter = self.request.user
        f.save()

        return super(CreateView, self).form_valid(form)

class LinkUpdateView(UpdateView):
    model = Link
    form_class = LinkForm

class LinkDeleteView(DeleteView):
    model = Link
    success_url = reverse_lazy("home")

class UserProfileDetailView(DetailView):
    model = get_user_model()
    slug_field = "username"
    template_name = "user_detail.html"

    def get_object(self, queryset=None):
        user = super(UserProfileDetailView, self).get_object(queryset)
        UserProfile.objects.get_or_create(user=user)
        return user


    

    
