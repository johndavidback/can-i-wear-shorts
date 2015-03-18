from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse

from .forms import SearchForm
import requests
import urllib
from json import loads


class HomeView(FormView):
    template_name = 'home.html'
    form_class = SearchForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):

        location = form.cleaned_data.get('location')

        # Let's get the shit
        base_url = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = "select item.condition from weather.forecast where woeid in " \
                    "(select woeid from geo.places(1) where text='%s')" % location
        yql_url = base_url + urllib.urlencode({'q': yql_query}) + '&format=json'

        data = requests.get(yql_url)
        content = loads(data.content)

        condition = content.get('query').get('results').get('channel').get('item').get('condition')
        temperature = int(condition.get('temp'))

        if temperature >= 65:
            result = 'Yeah, homie!'
        elif 50 <= temperature <= 64:
            result = 'Maybe, baby.'
        else:
            result = 'Nope.'

        context = super(HomeView, self).get_context_data()
        context['form'] = form
        context['results'] = {
            'result': result,
            'location': location,
            'temperature': temperature,
            'condition': condition.get('text'),
        }

        return self.render_to_response(context)
