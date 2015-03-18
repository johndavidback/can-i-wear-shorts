from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = ''

    def get_context_data(self, **kwargs):

        return {

        }
