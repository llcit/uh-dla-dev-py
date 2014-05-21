# oaiharvests/forms.py
from django import forms

class BrowseRepositoryForm(forms.Form):
    institutional_repo_name = forms.CharField()
    institutional_base_url = forms.CharField()
    set_identifier = forms.CharField()

    def display_results(self):
        # send email using the self.cleaned_data dictionary
        pass