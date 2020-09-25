from flask_admin.contrib.sqla import ModelView
from flask import session, redirect, url_for, request


class AdminView(ModelView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'statics'

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
