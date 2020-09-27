from datetime import datetime
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import typefmt
from flask import session, redirect, url_for, request


class AdminView(ModelView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'statics'
        print(self.date_format)
        self.column_formatters = dict(typefmt.BASE_FORMATTERS)
        self.column_formatters.update({
            type(None): typefmt.null_formatter,
            datetime: self.date_format,

        })

        self.column_type_formatters = self.column_formatters

    def date_format(self, view, value):
        return value.strftime('%B-%m-%Y %I:%M:%p')

    def is_accessible(self):
        return session.get('user') == 'george'

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('home', next=request.url))


class TopicView(AdminView):

    def __init__(self, *args, **kwargs):
        super(TopicView, self).__init__(*args, **kwargs)

    # List the various columns in the order you want them
    column_list = ('title', 'date_created', 'date_modified', 'status')
    # Columns that you want to be searchable in the model
    column_searchable_list = ('title',)
    # The column that the view should be sorted with by default
    column_default_sort = ('date_created', True)
    # List of columns that can be used to filter
    column_filters = ('status',)
