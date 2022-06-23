from django.shortcuts import render, redirect
from django.views import View
from .models import Building
from .forms import BuildingForm
from django.contrib import messages

class IndexView(View):
    def get(self, request, *args, **kwargs):

        context = {}
        context['buildings'] = Building.objects.all()
        # context = {
        #     'buildings': buildings
        # }

        return render(request, "student_management/index.html", context)


    def post(self, request, *args, **kwargs):
        
        form = BuildingForm(request.POST)

        if form.is_valid():
            form.save()
        else:
            messages.error(request, form.errors)

        # # modelsの方からの場合の書き方↓
        # posted = Building(name=request.POST["name"])
        # posted.save()

        return redirect("student_management:index")

index = IndexView.as_view()
