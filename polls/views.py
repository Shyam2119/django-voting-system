from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseForbidden
from .models import Election, Candidate, Vote
from .forms import VoteForm
import uuid

def home(request):
    # Display active elections on the homepage
    active_elections = Election.objects.filter(
        is_active=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    )
    
    upcoming_elections = Election.objects.filter(
        is_active=True,
        start_date__gt=timezone.now()
    )
    
    past_elections = Election.objects.filter(
        end_date__lt=timezone.now()
    )
    
    context = {
        'active_elections': active_elections,
        'upcoming_elections': upcoming_elections,
        'past_elections': past_elections,
    }
    
    return render(request, 'polls/home.html', context)

@login_required
def election_detail(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    
    # Check if the election is active
    if not election.is_ongoing():
        if election.has_ended():
            messages.info(request, 'This election has ended.')
            return redirect('election_results', election_id=election.id)
        else:
            messages.info(request, 'This election has not started yet.')
            return redirect('home')
    
    # Check if user has already voted
    if Vote.objects.filter(user=request.user, election=election).exists():
        messages.info(request, 'You have already voted in this election.')
        return redirect('vote_confirmation', election_id=election.id)
    
    if request.method == 'POST':
        form = VoteForm(election, request.POST)
        if form.is_valid():
            candidate = form.cleaned_data['candidate']
            # Generate unique verification code
            verification_code = str(uuid.uuid4())
            
            # Record the vote
            vote = Vote.objects.create(
                user=request.user,
                candidate=candidate,
                election=election,
                verification_code=verification_code
            )
            
            messages.success(request, 'Your vote has been recorded!')
            return redirect('vote_confirmation', election_id=election.id)
    else:
        form = VoteForm(election)
    
    context = {
        'election': election,
        'form': form,
    }
    
    return render(request, 'polls/election_detail.html', context)

@login_required
def vote_confirmation(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    
    try:
        vote = Vote.objects.get(user=request.user, election=election)
        context = {
            'election': election,
            'vote': vote,
        }
        return render(request, 'polls/vote_confirmation.html', context)
    except Vote.DoesNotExist:
        messages.error(request, 'You have not voted in this election yet.')
        return redirect('election_detail', election_id=election.id)

def election_results(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    
    # Only show results if the election has ended or the user is an admin
    if not election.has_ended() and not request.user.is_staff:
        messages.info(request, 'Results will be available after the election ends.')
        return redirect('home')
    
    candidates = election.candidates.all()
    results = []
    
    for candidate in candidates:
        votes_count = candidate.votes.count()
        results.append({
            'candidate': candidate,
            'votes': votes_count
        })
    
    # Sort results by votes (highest first)
    results.sort(key=lambda x: x['votes'], reverse=True)
    
    total_votes = Vote.objects.filter(election=election).count()
    
    context = {
        'election': election,
        'results': results,
        'total_votes': total_votes
    }
    
    return render(request, 'polls/election_results.html', context)

@login_required
def verify_vote(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        try:
            vote = Vote.objects.get(verification_code=verification_code)
            context = {
                'vote': vote,
                'verified': True
            }
            return render(request, 'polls/verify_vote.html', context)
        except Vote.DoesNotExist:
            messages.error(request, 'Invalid verification code.')
    
    return render(request, 'polls/verify_vote.html', {'verified': False})