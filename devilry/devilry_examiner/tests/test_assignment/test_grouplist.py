import htmls
from django import test
from django.conf import settings
from django_cradmin import cradmin_testhelpers
from model_mommy import mommy

from devilry.devilry_examiner.views.assignment import grouplist


class TestGroupItemValue(test.TestCase):
    def test_title(self):
        testgroup = mommy.make('core.AssignmentGroup')
        mommy.make('core.Candidate',
                   assignment_group=testgroup,
                   relatedstudent__user__fullname='Test User',
                   relatedstudent__user__shortname='testuser@example.com')
        selector = htmls.S(grouplist.GroupItemValue(value=testgroup).render())
        self.assertEqual(
            'Test User(testuser@example.com)',
            selector.one('.django-cradmin-listbuilder-itemvalue-titledescription-title').alltext_normalized)

    # def test_title_anonymous(self):
    #     testgroup = mommy.make('core.AssignmentGroup')
    #     mommy.make('core.Candidate',
    #                assignment_group=testgroup,
    #                relatedstudent__user__fullname='Test User',
    #                relatedstudent__user__shortname='testuser@example.com')
    #     selector = htmls.S(grouplist.GroupItemValue(value=testgroup).render())
    #     self.assertEqual(
    #         'Test User(testuser@example.com)',
    #         selector.one('.django-cradmin-listbuilder-itemvalue-titledescription-title').alltext_normalized)


class TestAssignmentListView(test.TestCase, cradmin_testhelpers.TestCaseMixin):
    viewclass = grouplist.GroupListView

    def test_title(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start',
                                           long_name='Assignment One')
        mommy.make('core.Examiner', relatedexaminer__user=testuser, user=testuser,
                   assignmentgroup__parentnode=testassignment)
        mockresponse = self.mock_http200_getrequest_htmls(cradmin_role=testassignment,
                                                          requestuser=testuser)
        self.assertIn(
            'Assignment One',
            mockresponse.selector.one('title').alltext_normalized)

    def test_h1(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start',
                                           long_name='Assignment One')
        mommy.make('core.Examiner', relatedexaminer__user=testuser, user=testuser,
                   assignmentgroup__parentnode=testassignment)
        mockresponse = self.mock_http200_getrequest_htmls(cradmin_role=testassignment,
                                                          requestuser=testuser)
        self.assertEqual(
            'Assignment One',
            mockresponse.selector.one('h1').alltext_normalized)

    def test_not_groups_where_not_examiner(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        mommy.make('core.Examiner',
                   assignmentgroup__parentnode=testassignment)
        mockresponse = self.mock_http200_getrequest_htmls(cradmin_role=testassignment,
                                                          requestuser=testuser)
        self.assertEqual(
            0,
            mockresponse.selector.count('.django-cradmin-listbuilder-itemvalue'))

    def test_groups_sanity(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        mommy.make('core.Examiner', relatedexaminer__user=testuser, user=testuser,
                   assignmentgroup__parentnode=testassignment)
        mommy.make('core.Examiner', relatedexaminer__user=testuser, user=testuser,
                   assignmentgroup__parentnode=testassignment)
        mockresponse = self.mock_http200_getrequest_htmls(cradmin_role=testassignment,
                                                          requestuser=testuser)
        self.assertEqual(
            2,
            mockresponse.selector.count('.django-cradmin-listbuilder-itemvalue'))

    def test_querycount(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        mommy.make('core.Examiner', relatedexaminer__user=testuser, user=testuser,
                   assignmentgroup__parentnode=testassignment,
                   _quantity=20)
        with self.assertNumQueries(2):
            self.mock_http200_getrequest_htmls(cradmin_role=testassignment,
                                               requestuser=testuser)

    def test_group_render_title_name_order(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        testgroup = mommy.make('core.AssignmentGroup', parentnode=testassignment)
        mommy.make('core.Examiner', relatedexaminer__user=testuser, user=testuser,
                   assignmentgroup=testgroup)
        mommy.make('core.Candidate',
                   assignment_group=testgroup,
                   relatedstudent__user__shortname='userb')
        mommy.make('core.Candidate',
                   assignment_group=testgroup,
                   relatedstudent__user__shortname='usera')
        mockresponse = self.mock_http200_getrequest_htmls(cradmin_role=testassignment,
                                                          requestuser=testuser)
        self.assertEqual(
            'usera , userb',
            mockresponse.selector.one(
                '.django-cradmin-listbuilder-itemvalue-titledescription-title').alltext_normalized)

    def test_group_render_title_name_order_fullname(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        testgroup = mommy.make('core.AssignmentGroup', parentnode=testassignment)
        mommy.make('core.Examiner', relatedexaminer__user=testuser, user=testuser,
                   assignmentgroup=testgroup)
        mommy.make('core.Candidate',
                   assignment_group=testgroup,
                   relatedstudent__user__shortname='userb')
        mommy.make('core.Candidate',
                   assignment_group=testgroup,
                   relatedstudent__user__shortname='userc',
                   relatedstudent__user__fullname='A user')
        mommy.make('core.Candidate',
                   assignment_group=testgroup,
                   relatedstudent__user__shortname='usera')
        mockresponse = self.mock_http200_getrequest_htmls(cradmin_role=testassignment,
                                                          requestuser=testuser)
        self.assertEqual(
            'A user(userc) , usera , userb',
            mockresponse.selector.one(
                '.django-cradmin-listbuilder-itemvalue-titledescription-title').alltext_normalized)

    # def test_render_search_nomatch(self):
    #     testuser = mommy.make(settings.AUTH_USER_MODEL)
    #     mommy.make('core.Examiner',
    #                relatedexaminer__user=testuser, user=testuser,
    #                assignmentgroup__parentnode=mommy.make_recipe(
    #                    'devilry.apps.core.assignment_activeperiod_start'))
    #     mockresponse = self.mock_http200_getrequest_htmls(
    #             cradmin_role=testassignment,
    #             viewkwargs={'filters_string': 'search-nomatch'},
    #             requestuser=testuser)
    #     self.assertEqual(
    #         0,
    #         mockresponse.selector.count('.django-cradmin-listbuilder-itemvalue-titledescription-title'))
    #
    # def test_render_search_match_subject_short_name(self):
    #     testuser = mommy.make(settings.AUTH_USER_MODEL)
    #     mommy.make('core.Examiner',
    #                relatedexaminer__user=testuser, user=testuser,
    #                assignmentgroup__parentnode=mommy.make_recipe(
    #                    'devilry.apps.core.assignment_activeperiod_start',
    #                    parentnode__parentnode__short_name='testsubject'))
    #     mockresponse = self.mock_http200_getrequest_htmls(
    #             cradmin_role=testassignment,
    #             viewkwargs={'filters_string': 'search-testsubject'},
    #             requestuser=testuser)
    #     self.assertEqual(
    #         1,
    #         mockresponse.selector.count('.django-cradmin-listbuilder-itemvalue-titledescription-title'))
    #
    # def test_render_search_match_subject_long_name(self):
    #     testuser = mommy.make(settings.AUTH_USER_MODEL)
    #     mommy.make('core.Examiner',
    #                relatedexaminer__user=testuser, user=testuser,
    #                assignmentgroup__parentnode=mommy.make_recipe(
    #                    'devilry.apps.core.assignment_activeperiod_start',
    #                    parentnode__parentnode__long_name='Testsubject'))
    #     mockresponse = self.mock_http200_getrequest_htmls(
    #             cradmin_role=testassignment,
    #             viewkwargs={'filters_string': 'search-Testsubject'},
    #             requestuser=testuser)
    #     self.assertEqual(
    #         1,
    #         mockresponse.selector.count('.django-cradmin-listbuilder-itemvalue-titledescription-title'))
    #
    # def test_render_search_match_period_short_name(self):
    #     testuser = mommy.make(settings.AUTH_USER_MODEL)
    #     mommy.make('core.Examiner',
    #                relatedexaminer__user=testuser, user=testuser,
    #                assignmentgroup__parentnode=mommy.make_recipe(
    #                    'devilry.apps.core.assignment_activeperiod_start',
    #                    parentnode__short_name='testperiod'))
    #     mockresponse = self.mock_http200_getrequest_htmls(
    #             cradmin_role=testassignment,
    #             viewkwargs={'filters_string': 'search-testperiod'},
    #             requestuser=testuser)
    #     self.assertEqual(
    #         1,
    #         mockresponse.selector.count('.django-cradmin-listbuilder-itemvalue-titledescription-title'))
    #
    # def test_render_search_match_period_long_name(self):
    #     testuser = mommy.make(settings.AUTH_USER_MODEL)
    #     mommy.make('core.Examiner',
    #                relatedexaminer__user=testuser, user=testuser,
    #                assignmentgroup__parentnode=mommy.make_recipe(
    #                    'devilry.apps.core.assignment_activeperiod_start',
    #                    parentnode__long_name='Testperiod'))
    #     mockresponse = self.mock_http200_getrequest_htmls(
    #             cradmin_role=testassignment,
    #             viewkwargs={'filters_string': 'search-Testperiod'},
    #             requestuser=testuser)
    #     self.assertEqual(
    #         1,
    #         mockresponse.selector.count('.django-cradmin-listbuilder-itemvalue-titledescription-title'))
    #
    # def test_render_search_match_assignment_short_name(self):
    #     testuser = mommy.make(settings.AUTH_USER_MODEL)
    #     mommy.make('core.Examiner',
    #                relatedexaminer__user=testuser, user=testuser,
    #                assignmentgroup__parentnode=mommy.make_recipe(
    #                    'devilry.apps.core.assignment_activeperiod_start',
    #                    short_name='testassignment'))
    #     mockresponse = self.mock_http200_getrequest_htmls(
    #             cradmin_role=testassignment,
    #             viewkwargs={'filters_string': 'search-testassignment'},
    #             requestuser=testuser)
    #     self.assertEqual(
    #         1,
    #         mockresponse.selector.count('.django-cradmin-listbuilder-itemvalue-titledescription-title'))
    #
    # def test_render_search_match_assignment_long_name(self):
    #     testuser = mommy.make(settings.AUTH_USER_MODEL)
    #     mommy.make('core.Examiner',
    #                relatedexaminer__user=testuser, user=testuser,
    #                assignmentgroup__parentnode=mommy.make_recipe(
    #                    'devilry.apps.core.assignment_activeperiod_start',
    #                    long_name='Testassignment'))
    #     mockresponse = self.mock_http200_getrequest_htmls(
    #             cradmin_role=testassignment,
    #             viewkwargs={'filters_string': 'search-Testassignment'},
    #             requestuser=testuser)
    #     self.assertEqual(
    #         1,
    #         mockresponse.selector.count('.django-cradmin-listbuilder-itemvalue-titledescription-title'))
    #
    # def __get_titles(self, selector):
    #     return [
    #         element.alltext_normalized
    #         for element in selector.list(
    #             '.django-cradmin-listbuilder-itemvalue-titledescription-title')]
    #
    # def test_render_orderby_default(self):
    #     testuser = mommy.make(settings.AUTH_USER_MODEL)
    #     testperiod1 = mommy.make_recipe('devilry.apps.core.period_active',
    #                                     parentnode__short_name='testsubject1',
    #                                     short_name='testperiod')
    #     testperiod2 = mommy.make_recipe('devilry.apps.core.period_active',
    #                                     parentnode__short_name='testsubject2',
    #                                     short_name='testperiod')
    #     mommy.make('core.Examiner',
    #                relatedexaminer__user=testuser, user=testuser,
    #                assignmentgroup__parentnode=mommy.make_recipe(
    #                    'devilry.apps.core.assignment_activeperiod_start',
    #                    long_name='Assignment 1',
    #                    publishing_time=ACTIVE_PERIOD_START + timedelta(days=1),
    #                    parentnode=testperiod1))
    #     mommy.make('core.Examiner',
    #                relatedexaminer__user=testuser, user=testuser,
    #                assignmentgroup__parentnode=mommy.make_recipe(
    #                    'devilry.apps.core.assignment_activeperiod_start',
    #                    long_name='Assignment 2',
    #                    publishing_time=ACTIVE_PERIOD_START + timedelta(days=3),
    #                    parentnode=testperiod1))
    #     mommy.make('core.Examiner',
    #                relatedexaminer__user=testuser, user=testuser,
    #                assignmentgroup__parentnode=mommy.make_recipe(
    #                    'devilry.apps.core.assignment_activeperiod_start',
    #                    long_name='Assignment 1',
    #                    publishing_time=ACTIVE_PERIOD_START + timedelta(days=2),
    #                    parentnode=testperiod2))
    #     mockresponse = self.mock_http200_getrequest_htmls(
    #             cradmin_role=testassignment,
    #             requestuser=testuser)
    #     self.assertEqual(
    #         [
    #             'testsubject1.testperiod - Assignment 2',
    #             'testsubject2.testperiod - Assignment 1',
    #             'testsubject1.testperiod - Assignment 1',
    #         ],
    #         self.__get_titles(mockresponse.selector))
    #
    # def test_render_orderby_publishing_time_descending(self):
    #     testuser = mommy.make(settings.AUTH_USER_MODEL)
    #     testperiod1 = mommy.make_recipe('devilry.apps.core.period_active',
    #                                     parentnode__short_name='testsubject1',
    #                                     short_name='testperiod')
    #     testperiod2 = mommy.make_recipe('devilry.apps.core.period_active',
    #                                     parentnode__short_name='testsubject2',
    #                                     short_name='testperiod')
    #     mommy.make('core.Examiner',
    #                relatedexaminer__user=testuser, user=testuser,
    #                assignmentgroup__parentnode=mommy.make_recipe(
    #                    'devilry.apps.core.assignment_activeperiod_start',
    #                    long_name='Assignment 1',
    #                    publishing_time=ACTIVE_PERIOD_START + timedelta(days=1),
    #                    parentnode=testperiod1))
    #     mommy.make('core.Examiner',
    #                relatedexaminer__user=testuser, user=testuser,
    #                assignmentgroup__parentnode=mommy.make_recipe(
    #                    'devilry.apps.core.assignment_activeperiod_start',
    #                    long_name='Assignment 2',
    #                    publishing_time=ACTIVE_PERIOD_START + timedelta(days=3),
    #                    parentnode=testperiod1))
    #     mommy.make('core.Examiner',
    #                relatedexaminer__user=testuser, user=testuser,
    #                assignmentgroup__parentnode=mommy.make_recipe(
    #                    'devilry.apps.core.assignment_activeperiod_start',
    #                    long_name='Assignment 1',
    #                    publishing_time=ACTIVE_PERIOD_START + timedelta(days=2),
    #                    parentnode=testperiod2))
    #     mockresponse = self.mock_http200_getrequest_htmls(
    #             cradmin_role=testassignment,
    #             viewkwargs={'filters_string': 'orderby-publishing_time_descending'},
    #             requestuser=testuser)
    #     self.assertEqual(
    #         [
    #             'testsubject1.testperiod - Assignment 1',
    #             'testsubject2.testperiod - Assignment 1',
    #             'testsubject1.testperiod - Assignment 2',
    #         ],
    #         self.__get_titles(mockresponse.selector))
    #
    # def test_render_orderby_name_ascending(self):
    #     testuser = mommy.make(settings.AUTH_USER_MODEL)
    #     testperiod1 = mommy.make_recipe('devilry.apps.core.period_active',
    #                                     parentnode__short_name='testsubject1',
    #                                     short_name='testperiod')
    #     testperiod2 = mommy.make_recipe('devilry.apps.core.period_active',
    #                                     parentnode__short_name='testsubject2',
    #                                     short_name='testperiod')
    #     mommy.make('core.Examiner',
    #                relatedexaminer__user=testuser, user=testuser,
    #                assignmentgroup__parentnode=mommy.make_recipe(
    #                    'devilry.apps.core.assignment_activeperiod_start',
    #                    long_name='Assignment 1',
    #                    parentnode=testperiod1))
    #     mommy.make('core.Examiner',
    #                relatedexaminer__user=testuser, user=testuser,
    #                assignmentgroup__parentnode=mommy.make_recipe(
    #                    'devilry.apps.core.assignment_activeperiod_start',
    #                    long_name='Assignment 1',
    #                    parentnode=testperiod2))
    #     mommy.make('core.Examiner',
    #                relatedexaminer__user=testuser, user=testuser,
    #                assignmentgroup__parentnode=mommy.make_recipe(
    #                    'devilry.apps.core.assignment_activeperiod_start',
    #                    long_name='Assignment 2',
    #                    parentnode=testperiod1))
    #     mockresponse = self.mock_http200_getrequest_htmls(
    #             cradmin_role=testassignment,
    #             requestuser=testuser,
    #             viewkwargs={'filters_string': 'orderby-name_ascending'})
    #     self.assertEqual(
    #         [
    #             'testsubject1.testperiod - Assignment 1',
    #             'testsubject1.testperiod - Assignment 2',
    #             'testsubject2.testperiod - Assignment 1',
    #         ],
    #         self.__get_titles(mockresponse.selector))
    #
    # def test_render_orderby_name_descending(self):
    #     testuser = mommy.make(settings.AUTH_USER_MODEL)
    #     testperiod1 = mommy.make_recipe('devilry.apps.core.period_active',
    #                                     parentnode__short_name='testsubject1',
    #                                     short_name='testperiod')
    #     testperiod2 = mommy.make_recipe('devilry.apps.core.period_active',
    #                                     parentnode__short_name='testsubject2',
    #                                     short_name='testperiod')
    #     mommy.make('core.Examiner',
    #                relatedexaminer__user=testuser, user=testuser,
    #                assignmentgroup__parentnode=mommy.make_recipe(
    #                    'devilry.apps.core.assignment_activeperiod_start',
    #                    long_name='Assignment 1',
    #                    parentnode=testperiod1))
    #     mommy.make('core.Examiner',
    #                relatedexaminer__user=testuser, user=testuser,
    #                assignmentgroup__parentnode=mommy.make_recipe(
    #                    'devilry.apps.core.assignment_activeperiod_start',
    #                    long_name='Assignment 1',
    #                    parentnode=testperiod2))
    #     mommy.make('core.Examiner',
    #                relatedexaminer__user=testuser, user=testuser,
    #                assignmentgroup__parentnode=mommy.make_recipe(
    #                    'devilry.apps.core.assignment_activeperiod_start',
    #                    long_name='Assignment 2',
    #                    parentnode=testperiod1))
    #     mockresponse = self.mock_http200_getrequest_htmls(
    #             cradmin_role=testassignment,
    #             requestuser=testuser,
    #             viewkwargs={'filters_string': 'orderby-name_descending'})
    #     self.assertEqual(
    #         [
    #             'testsubject2.testperiod - Assignment 1',
    #             'testsubject1.testperiod - Assignment 2',
    #             'testsubject1.testperiod - Assignment 1',
    #         ],
    #         self.__get_titles(mockresponse.selector))
    #