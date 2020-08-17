from wtforms import widgets, TextAreaField


class CKEditorTextArea(widgets.TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKEditorTextArea, self).__call__(field, **kwargs)


class CKTextArea(TextAreaField):
    widget = CKEditorTextArea()
