import urllib
from json import loads

from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy
import requests

from .forms import SearchForm


class HomeView(FormView):
    template_name = 'home.html'
    form_class = SearchForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):

        location = form.cleaned_data.get('location')

        context = super(HomeView, self).get_context_data()
        context['form'] = form

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
            result = 'Yeah, homie!'
        elif 50 <= temperature <= 64:
            result = 'Maybe, baby.'
        else:
            result = 'Nope.'

        context['results'] = {
            'result': result,
            'location': location,
            'temperature': temperature,
            'condition': condition,
        }

        return self.render_to_response(context)
