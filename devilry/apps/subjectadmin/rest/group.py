from devilry.rest.indata import indata
from devilry.rest.restbase import RestBase

from devilry.apps.core.models import (Assignment,
                                      AssignmentGroup,
                                      AssignmentGroupTag,
                                      Candidate,
                                      Examiner
                                     )

from errors import PermissionDeniedError



class AssignmentadminRequiredError(PermissionDeniedError):
    """
    Raised to signal that a subject admin is required for the given operation.
    """


def assignmentadmin_required(user, errormsg, *assignmentids):
    if user.is_superuser:
        return
    for assignmentid in assignmentids:
        if assignmentid == None:
            raise AssignmentadminRequiredError(errormsg)
        if Assignment.where_is_admin(user).filter(id=assignmentid).count() == 0:
            raise AssignmentadminRequiredError(errormsg)


class GroupDao(object):
    """
    Makes it convenient to work with everything related to an AssignmentGroup:

    - name
    - is_open
    - feedback
    - tags
    - deadlines
    - Candidates (students)
        - Candidate ID
        - Username
        - Full name
        - Email
    - Examiners
        - Username
        - Full name
        - Email
    """

    def _get_groups(self, assignmentid):
        """
        Get a list of group dictionaries.
        """
        fields = ('id', 'name', 'is_open', 'feedback__grade', 'feedback__points',
                  'feedback__is_passing_grade', 'feedback__save_timestamp')
        groups = AssignmentGroup.objects.filter(parentnode=assignmentid).select_related('feedback').values(*fields)
        return groups

    def _prepare_group(self, group):
        """ Add the separate-query-aggreagated fields to the group dict. """
        group['tags'] = []
        group['students'] = []
        group['examiners'] = []
        return group

    def _convert_groupslist_to_groupsdict(self, groups):
        groupsdict = {}
        for group in groups:
            groupsdict[group['id']] = self._prepare_group(group)
        return groupsdict

    def _merge_tags_with_groupsdict(self, tags, groupsdict):
        for tagdict in tags:
            group = groupsdict[tagdict['assignment_group_id']]
            group['tags'].append(tagdict['tag'])

    def _merge_with_groupsdict(self, groupsdict, listofdicts, targetkey, assignmentgroup_key='assignment_group_id'):
        for dct in listofdicts:
            group = groupsdict[dct[assignmentgroup_key]]
            del dct[assignmentgroup_key]
            group[targetkey].append(dct)

    def _get_candidates(self, assignmentid):
        fields = ('assignment_group_id', 'candidate_id',
                  'student__username', 'student__email',
                  'student__devilryuserprofile__full_name')
        return Candidate.objects.filter(assignment_group__parentnode=assignmentid).values(*fields)

    def _get_examiners(self, assignmentid):
        fields = ('assignmentgroup_id',
                  'user__username', 'user__email',
                  'user__devilryuserprofile__full_name')
        return Examiner.objects.filter(assignmentgroup__parentnode=assignmentid).values(*fields)

    def _get_tags(self, assignmentid):
        fields = ('assignment_group_id', 'tag')
        return AssignmentGroupTag.objects.filter(assignment_group__parentnode=assignmentid).values(*fields)

    def read(self, user, assignmentid):
        assignmentadmin_required(user, "i18n.permissiondenied", assignmentid)
        groups = self._get_groups(assignmentid)
        groupsdict = self._convert_groupslist_to_groupsdict(groups)

        tags = self._get_tags(assignmentid)
        self._merge_tags_with_groupsdict(tags, groupsdict)

        candidates = self._get_candidates(assignmentid)
        self._merge_with_groupsdict(groupsdict, candidates, 'students')

        examiners = self._get_examiners(assignmentid)
        self._merge_with_groupsdict(groupsdict, examiners, 'examiners', assignmentgroup_key='assignmentgroup_id')

        for group in groupsdict.values():
            print group


#class Group(RestBase):
    #def __init__(self, daocls=NodeDao, **basekwargs):
        #super(Group, self).__init__(**basekwargs)
        #self.dao = daocls()

    #def todict(self, node):
        #item = node
        #links = {}
        #links['toplevel-nodes'] = self.geturl()
        #if node['parentnode_id'] != None:
            #links['parentnode'] = self.geturl(node['parentnode_id'])
        #links['childnodes'] = self.geturl(params={'id': node['id']})
        #links['node'] = self.geturl(node['id'])
        #return dict(
            #item=item,
            #links=links
        #)

    #@indata(id=int)
    #def read(self, id):
        #return self.todict(self.dao.read(self.user, id))

    #@indata(short_name=unicode, long_name=unicode)
    #def create(self, short_name, long_name):
        #return self.todict(self.dao.create(self.user, short_name, long_name))

    #@indata(id=int, short_name=unicode, long_name=unicode)
    #def update(self, id, short_name, long_name):
        #return self.todict(self.dao.update(self.user, id, short_name, long_name))

    #@indata(id=int)
    #def list(self, id=None):
        #items = self._get_items(id)
        #return dict(
            #params=dict(
                #parentnode_id=id
            #),
            #links=self.get_links(id),
            #items=items,
            #total=len(items)
        #)

    ##    @indata(parentnode_id=force_list)
##    def batch(self, create=[], update=[], delete=[]):
##        for kw in create:
##            self.create(**kw)
##        for kw in update:
##            self.update(**kw)
##        for kw in delete:
##            self.delete(**kw)

    #def _get_items(self, parentnode_id):
        #return [self.todict(item) for item in self.dao.list(self.user, parentnode_id)]

    #def get_links(self, id):
        #links = {}
        #if id:
            #links['node'] = self.geturl(id)
        #return links
