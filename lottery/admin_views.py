import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .forms import LotteryUploadForm
from .serializers import LotterySerializer

@staff_member_required
def lottery_upload_view(request):
    """
    Admin view to paste lottery JSON directly into a text area.
    Only accessible to authenticated staff users.
    """
    if request.method == "POST":
        form = LotteryUploadForm(request.POST)
        if form.is_valid():
            json_text = form.cleaned_data["json_text"]
            try:
                data = json.loads(json_text)
                serializer = LotterySerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    messages.success(request, "Lottery JSON uploaded successfully!")
                    return redirect("admin:index")
                else:
                    messages.error(request, f"Validation Error: {serializer.errors}")
            except Exception as e:
                messages.error(request, f"Invalid JSON: {e}")
    else:
        form = LotteryUploadForm()

    return render(request, "admin/lottery_upload.html", {"form": form})
