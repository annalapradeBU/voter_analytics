# File: views.py
# Author: Anna LaPrade (alaprade@bu.edu), 10/28/2025
# Description: the view functions for the pages of the voter_analytics app

from django.shortcuts import render
from django.db.models.query import QuerySet
from django.shortcuts import render 
from django.views.generic import ListView, DetailView
from . models import Voter
from .forms import VoterFilterForm
# import plotly for graphing
import plotly 
import plotly.graph_objs as go 
from django.db.models import Count, Q

# Create your views here.

# class to faciliate viewing all the Voter objects
class VotersListView(ListView):
    '''View to display voters'''
 
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by= 100
 
    # allow filtering 
    def get_queryset(self):
        # by default, sort by last name 
        voters = super().get_queryset().order_by('last_name', 'pk')
        form = VoterFilterForm(self.request.GET)

        if form.is_valid():
            data = form.cleaned_data

            # if one of these things is specified, filter for it
            if data.get('party_affiliation'):
                party = data['party_affiliation']
                print("Filtering party:", repr(party))
                voters = voters.filter(party_affiliation__iexact=data['party_affiliation'])
            
            if data.get('min_dob'):
                voters = voters.filter(date_of_birth__year__gte=int(data['min_dob']))
            
            if data.get('max_dob'):
                voters = voters.filter(date_of_birth__year__lte=int(data['max_dob']))
            
            if data.get('voter_score'):
                voters = voters.filter(voter_score=int(data['voter_score']))

            # elections
            for election_field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
                if data.get(election_field):
                    voters = voters.filter(**{election_field: True})

        return voters
    
    # get the context 
    def get_context_data(self, **kwargs):
        '''get the contect data for the VotersListView to pass to template'''
        context = super().get_context_data(**kwargs)
        # pass the form into the template context
        context['filter_form'] = VoterFilterForm(self.request.GET)

        # get rid of page info so it doesn't keep adding page parameters 
        query_dict = self.request.GET.copy()
        if 'page' in query_dict:
            query_dict.pop('page')

        # pass in query to keep consistent accross pages
        context['query_params'] = query_dict.urlencode()

        return context
    

# show a specific Voter and their attributes
class VoterDetailView(DetailView):
    '''display voters for a single runner'''

    model = Voter
    context_object_name = 'v' # short for voter
    template_name = 'voter_analytics/voter_detail.html'


# view that facilitates viewing graph analytics 
class GraphView(ListView):
    ''' faciliates the creation and display of voter analytic graphs'''
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    # allow filtering 
    def get_queryset(self):
        form = VoterFilterForm(self.request.GET)
        if form.is_valid():
            qs = Voter.objects.all()

            # if one of these things is specified, filter for it
            party = form.cleaned_data.get("party_affiliation")
            if party:
                qs = qs.filter(party_affiliation=party)

            min_dob = form.cleaned_data.get("min_dob")
            if min_dob:
                qs = qs.filter(date_of_birth__year__gte=min_dob)

            max_dob = form.cleaned_data.get("max_dob")
            if max_dob:
                qs = qs.filter(date_of_birth__year__lte=max_dob)

            score = form.cleaned_data.get("voter_score")
            if score:
                qs = qs.filter(voter_score=score)

            for election_field in ["v20state","v21town","v21primary","v22general","v23town"]:
                if form.cleaned_data.get(election_field):
                    kwargs = {election_field: True}
                    qs = qs.filter(**kwargs)

            return qs
        return Voter.objects.all()

    # get context for this view
    def get_context_data(self, **kwargs):
        ''' get contect data for the graph view '''

        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()
        context["filter_form"] = VoterFilterForm(self.request.GET)
        context['elections'] = ['v20state','v21town','v21primary','v22general','v23town']
        

        # --- birth Year distribution ---
        birth_counts = {}

        # increment birth year count when enountered
        for year in voters.values_list('date_of_birth__year', flat=True):
            if year:
                birth_counts[year] = birth_counts.get(year, 0) + 1

        # graph the birth count histogram
        if birth_counts:
            x = list(birth_counts.keys())
            y = list(birth_counts.values())
            fig = go.Bar(x=x, y=y)
            graph_div_birth = plotly.offline.plot({"data": [fig],
                                    "layout_title_text": "Voter Birth Year Distribution"},
                                   auto_open=False, output_type="div")
        # otherwise, say nothing available
        else:
            graph_div_birth = "<p>No data available.</p>"
        context["birth_graph"] = graph_div_birth

        # Graph the party affiliation pie chart 
        party_counts = voters.values('party_affiliation').annotate(total=Count('party_affiliation'))
        if party_counts:
            x = [p['party_affiliation'] or 'None' for p in party_counts]
            y = [p['total'] for p in party_counts]
            fig = go.Pie(labels=x, values=y)
            graph_div_party = plotly.offline.plot({"data": [fig],
                                    "layout_title_text": "Voters by Party Affiliation"},
                                   auto_open=False, output_type="div")
        # otherwise, say nothing available
        else:
            graph_div_party = "<p>No data available.</p>"
        context["party_graph"] = graph_div_party

        # graph election participation bar charts
        participation = {
            '2020 State': voters.filter(v20state=True).count(),
            '2021 Town': voters.filter(v21town=True).count(),
            '2021 Primary': voters.filter(v21primary=True).count(),
            '2022 General': voters.filter(v22general=True).count(),
            '2023 Town': voters.filter(v23town=True).count(),
        }
        if any(participation.values()):
            x = list(participation.keys())
            y = list(participation.values())
            fig = go.Bar(x=x, y=y)
            graph_div_participation = plotly.offline.plot({"data": [fig],
                                            "layout_title_text": "Voter Participation by Election"},
                                           auto_open=False, output_type="div")
         # otherwise, say nothing available
        else:
            graph_div_participation = "<p>No data available.</p>"
        context["participation_graph"] = graph_div_participation

        return context