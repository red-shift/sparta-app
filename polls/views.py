from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Q

from .models import Event, Fighter, Match

from .forms import EventForm, FighterForm, MatchForm, VoteMatchForm

from datetime import datetime
import re


# from .models import
# Create your views here.
"""
Public Views
"""


def find_fighter_match_relationship(matches, fighters):
    # Iterate through fighters and matches to see if a match has a fighter's id
    for f in fighters:
        for m in matches:
            if m.red_corner_id == f.id or m.blue_corner_id == f.id:
                continue
            else:
                fighters = fighters.exclude(pk=f.id)
    return fighters


class IndexView(View):
    template_name = 'sparta/public/index.html'

    def get(self, request):
        #self.reset_session_votes(request)
        events = Event.objects.all()
        c = {
            'events': events,
        }
        return render(request, self.template_name, c)

    def reset_session_votes(self, request):
        request.session['fvote'] = False
        request.session['pvote'] = False
        request.session.modified = True


class FightPollView(View):
    template_name = 'sparta/forms/vote-match.html'

    # Display blank ass form
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        if event.poll_status == 'Closed':
            return redirect('sparta:index')
        matches = Match.objects.all().filter(event_id=event.id)
        c = {
            'event': event,
            'matches': matches
        }
        return render(request, self.template_name, c)

    # Process the fucking form data
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        if event.poll_status == 'Closed':
            return redirect('sparta:index')
        matches = Match.objects.all().filter(event_id=event.id)
        c = {
            'matches': matches,
        }

        match_id = request.POST.get('vote', None)
        if match_id is None:
            messages.error(request, "You did not vote!", extra_tags='alert alert-danger')
            return render(request, self.template_name, c)
        else:
            match = get_object_or_404(Match, pk=match_id)
            request.session['fvote'] = event.id
            match.save()
            messages.success(request, 'Thank you for participating', extra_tags='alert alert-primary')
            return redirect('sparta:fight-index', pk)


class PerformancePollView(View):
    template_name = 'sparta/forms/vote-performance.html'

    # Display blank ass form
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        matches = Match.objects.all().filter(event_id=event.id)
        fighters = Fighter.objects.all().filter(event_id=event.id)
        # Iterate through fighters and matches to see if a match has a fighter's id
        fighters = find_fighter_match_relationship(matches, fighters)
        c = {
            'event': event,
            'fighters': fighters
        }
        return render(request, self.template_name, c)

    # Process the fucking form data
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        fighters = Fighter.objects.all().filter(event_id=event.id)
        c = {
            'fighters': fighters
        }

        fighter_id = request.POST.get('vote', None)
        if fighter_id is None:
            messages.error(request, "You did not vote!", extra_tags='alert alert-danger')
            return render(request, self.template_name, c)
        else:
            fighter = get_object_or_404(Fighter, pk=fighter_id)
            request.session['pvote'] = event.id
            fighter.votes += 1
            fighter.save()
            messages.success(request, 'Thank you for participating', extra_tags='alert alert-primary')
            return redirect('sparta:performance-index', pk)


class PollsQuickView(LoginRequiredMixin, View):
    login_url = reverse_lazy('sparta:login')
    template_name = 'sparta/admin/polls-quick-view.html'

    def get(self, request):
        # Lookups that span relationships see:
        # https://docs.djangoproject.com/en/1.9/topics/db/queries/#s-lookups-that-span-relationships
        matches = Match.objects.all().filter(event__poll_status='Open').order_by('-votes')
        fighters = Fighter.objects.all().filter(event__poll_status='Open').order_by('-votes')
        # Iterate through fighters and matches to see if a match has a fighter's id
        fighters = find_fighter_match_relationship(matches, fighters)
        c = {
            'matches': matches,
            'fighters': fighters,

        }

        return render(request, self.template_name, c)

"""
Admin Views
"""


class SpartaAdminView(LoginRequiredMixin, View):
    login_url = reverse_lazy('sparta:login')
    template_name = 'sparta/sitebase/base-admin.html'

    def get(self, request):
        return render(request, self.template_name)


class ManageEventsView(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('sparta:login')
    model = Event
    template_name = 'sparta/admin/manage-events.html'
    context_object_name = 'events'


class AddEventView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('sparta:login')
    form_class = EventForm
    template_name = 'sparta/forms/add-event.html'
    success_message = 'Event was added successfully'
    success_url = reverse_lazy('sparta:manage-events')


class UpdateEventView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('sparta:login')
    model = Event
    form_class = EventForm
    template_name = 'sparta/forms/update-event.html'
    success_message = 'Event was successfully updated'
    success_url = reverse_lazy('sparta:manage-events')


class DeleteEventView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('sparta:login')
    model = Event
    success_message = 'Event has been deleted'
    success_url = reverse_lazy('sparta:manage-events')

    #  SuccessMessageMixin does not work for DeleteView, therefore you must override delete and use messages
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteEventView, self).delete(request, *args, **kwargs)


class ManageFightersView(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('sparta:login')
    model = Fighter
    template_name = 'sparta/admin/manage-fighters.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ManageFightersView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['fighters'] = Fighter.objects.all().order_by('-votes')
        return context


class AddFighterView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('sparta:login')
    form_class = FighterForm
    template_name = 'sparta/forms/add-fighter.html'
    success_message = 'Fighter was added successfully'
    success_url = reverse_lazy('sparta:manage-fighters')


class UpdateFighterView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('sparta:login')
    model = Fighter
    form_class = FighterForm
    template_name = 'sparta/forms/update-fighter.html'
    success_message = 'Fighter was successfully updated'
    success_url = reverse_lazy('sparta:manage-fighters')


class DeleteFighterView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('sparta:login')
    model = Fighter
    success_message = 'Fighter has been deleted'
    success_url = reverse_lazy('sparta:manage-fighters')

    #  SuccessMessageMixin does not work for DeleteView, therefore you must override delete and use messages
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteFighterView, self).delete(request, *args, **kwargs)


class ManageMatchesView(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('sparta:login')
    model = Match
    template_name = 'sparta/admin/manage-matches.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ManageMatchesView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['matches'] = Match.objects.all().order_by('-votes')
        return context


class AddMatchView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('sparta:login')
    form_class = MatchForm
    template_name = 'sparta/forms/add-match.html'
    success_message = 'Match was added successfully'
    success_url = reverse_lazy('sparta:manage-matches')

    def get_context_data(self, **kwargs):
        events = Event.objects.all()
        context = super(AddMatchView, self).get_context_data(**kwargs)
        context['events'] = events
        return context


class UpdateMatchView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('sparta:login')
    model = Match
    form_class = MatchForm
    template_name = 'sparta/forms/update-match.html'
    success_message = 'Match was successfully updated'
    success_url = reverse_lazy('sparta:manage-matches')


class DeleteMatchView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('sparta:login')
    model = Match
    success_message = 'Match has been deleted'
    success_url = reverse_lazy('sparta:manage-matches')

    #  SuccessMessageMixin does not work for DeleteView, therefore you must override delete and use messages
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteMatchView, self).delete(request, *args, **kwargs)




"""
Site access views
"""


class LoginView(View):
    template_name = 'sparta/forms/login.html'

    # Display blank ass form
    def get(self, request):
        if request.user.is_authenticated():
            return redirect('sparta:manage-events')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('sparta:manage-events')
            else:
                messages.error(request, "Your account is not active, please contact an administrator",
                               extra_tags='alert alert-danger')
                return render(request, self.template_name)
        else:
            messages.error(request, "Username/Password is invalid", extra_tags='alert alert-danger')
            return render(request, self.template_name)

        return render(request, self.template_name)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('sparta:login')

