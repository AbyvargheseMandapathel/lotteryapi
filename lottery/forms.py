from django import forms

class LotteryUploadForm(forms.Form):
    json_text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 20, "cols": 100}),
        label="Paste Lottery JSON here"
    )
