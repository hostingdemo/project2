from django import forms

from cms_dashboard.models import CSVFile


class ImportFileForm(forms.ModelForm):
    class Meta:
        model = CSVFile
        fields = ('csv_file',)

        widgets = {
            'csv_file': forms.TextInput(attrs={
                'type': 'file', 
                'id': 'customFile', 
                'class': 'custom-file-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super(ImportFileForm, self).__init__(*args, **kwargs)
        self.fields['csv_file'].label = ""
