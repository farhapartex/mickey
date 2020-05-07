from django import forms

class HtmlEditor(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super(HtmlEditor, self).__init__(*args, **kwargs)
        self.attrs['class'] = 'html-editor'

    class Media:
        # css = {
        #     'all': (
        #         'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.9.0/codemirror.css',
        #     )
        # }
        js = (
            'https://cdn.tiny.cloud/1/no-api-key/tinymce/5/tinymce.min.js',
            '/static/tinymce/init.js'
        )