from django_cradmin import crapp
from devilry.apps.core.models import Subject
from devilry.devilry_admin.views.common import admins_common


class PermissionMixin(object):
    model = Subject.admins.through
    basenodefield = 'subject'


class AdminsListView(PermissionMixin, admins_common.AbstractAdminsListView):
    pass


class RemoveAdminView(PermissionMixin, admins_common.AbstractRemoveAdminView):
    pass


class App(crapp.App):
    appurls = [
        crapp.Url(r'^$', AdminsListView.as_view(), name=crapp.INDEXVIEW_NAME),
        crapp.Url(
            r'^remove/(?P<pk>\d+)$',
            RemoveAdminView.as_view(),
            name="remove"),
    ]