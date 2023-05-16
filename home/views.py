from django.views.generic import ListView


# Create your views here.
class BaseListView(ListView):
    paginate_by = 10
    paginate_orphans = 5
    