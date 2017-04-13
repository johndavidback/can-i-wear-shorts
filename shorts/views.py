import urllib
from json import loads

from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy
import requests
from django.conf import settings

from .forms import SearchForm
from random import choice


YES = [
    'Hell yeah!',
    'Si',
    'Yeah, homie',
    'Fo sho',
    'Aye, aye, cap\'n',
    'Hey girl, you wear them shorts',
    'Totes',
    'Duh.'
]

NO = [
    'Hell no.',
    'Not a good idea.',
    'How about no.',
    'No way, Jose.',
    'Nein.',
    'Uhhh no.',
    'Nah, G.'
]


class HomeView(FormView):
    template_name = 'home.html'
    form_class = SearchForm
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        form = self.get_form_class()(self.request.GET or None)

        if form.is_valid():
            return self.process_form(form)

        else:
            context = super(HomeView, self).get_context_data(**kwargs)
            context['form'] = form
            context['BASE_URL'] = settings.BASE_URL

            return self.render_to_response(context)

    def form_valid(self, form):

        self.process_form(form)

    def process_form(self, form):
        context = super(HomeView, self).get_context_data()
        context['form'] = form

        location = form.cleaned_data.get('location')

        # Let's get the shit
        base_url = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = "select item.condition from weather.forecast where woeid in " \
                    "(select woeid from geo.places(1) where text='%s')" % location
        yql_url = base_url + urllib.urlencode({'q': yql_query}) + '&format=json'

        data = requests.get(yql_url)
        content = loads(data.content)

        try:
            conditions = content.get('query').get('results').get('channel').get('item').get('condition')
            temperature = int(conditions.get('temp'))
            condition = conditions.get('text')
        except AttributeError:
            context['error'] = "Does that place exist?"
            return self.render_to_response(context)

        if temperature >= 65:
            result = choice(YES)
        elif 50 <= temperature <= 64:
            result = 'Maybe, baby.'
        else:
            result = choice(NO)

        context['results'] = {
            'result': result,
            'location': location,
            'temperature': temperature,
            'condition': condition,
        }

        context['BASE_URL'] = settings.BASE_URL

        return self.render_to_response(context)
