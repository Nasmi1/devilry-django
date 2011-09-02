import json
from django.conf import settings

from devilry.apps.gradeeditors import (gradeeditor_registry, JsonRegistryItem,
                                       DraftValidationError, ConfigValidationError)
from devilry.apps.markup.parse_markdown import markdown_full



class BasicForm(JsonRegistryItem):
    gradeeditorid = 'basicform'
    title = 'Basicform Editor'
    description = 'An editor where admin can set up different fields for feedback for different parts of an assignment'
    config_editor_url = settings.DEVILRY_STATIC_URL + '/basicform_gradeeditor/configeditor.js'
    draft_editor_url = settings.DEVILRY_STATIC_URL + '/basicform_gradeeditor/drafteditor.js'

    @classmethod
    def validate_draft(cls, draftstring, configstring):
        draft = json.loads(draftstring)
        config = json.loads(configstring)

        cls.validate_dict(draft, DraftValidationError, {'values': list,
                                                        'feedback': basestring})
        cls.validate_gradeeditor_key(draft, 'basicform')

        gradeeditor = draft['gradeeditor']
        draftval = draft['values']
        confval = config['formValues']

        for i in xrange(0, len(draftval)):
            if confval[i][0]=='check':
                if not isinstance(draftval[i], bool):
                    errormsg = 'the field labled "' + confval[i][2] + '" has to contain a boolean-value'
                    raise ConfigValidationError(errormsg)

            elif confval[i][0] == 'number':
                if not isinstance(draftval[i], int):
                    errormsg = 'the field labled "' + confval[i][2] + '" has to contain a number 0 or higher'
                    raise ConfigValidationError(errormsg)

                if draftval[i]<0:
                    errormsg = 'the field labled "' + confval[i][2] + '" has to contain a number 0 or higher'
                    raise ConfigValidationError(errormsg)

    @classmethod
    def validate_config(cls, configstring):
        config = cls.decode_configstring(configstring)

        form = config['formValues']
        approvedLimit = config['approvedLimit']

        if len(form) == 0:
            raise ConfigValidationError('You have to specify at least one form-field')

        pointSum = 0
        for entry in form:
            if len(entry) != 3:
                raise ConfigValidationError('You have to specify fieldtype, points and label')

            if not isinstance(entry[0], basestring):
                raise ConfigValidationError('You have to specify fieldtype as either "number" or "check"')

            if entry[0] != 'number' and entry[0] != 'check':
                raise ConfigValidationError('You have to specify fieldtype as either "number" or "check"')

            if entry[1] == '':
                raise ConfigValidationError('You have to enter points as a number 0 or higher')

            if int(entry[1])<0:
                raise ConfigValidationError('You have to enter points as a number 0 or higher')

            if not isinstance(entry[2], basestring):
                raise ConfigValidationError('You have to enter the field-label as plain text')

            if entry[2] == '':
                raise ConfigValidationError('You have to enter a field-label')

            pointSum+=int(entry[1])

        if not isinstance(approvedLimit, int):
                raise ConfigValidationError('You have to enter points to pass as a number 0 or higher')

        if approvedLimit < 0:
                raise ConfigValidationError('You have to enter points to pass as a number 0 or higher')

        if approvedLimit>pointSum:
            raise ConfigValidationError('Points to pass has to be equal to, or smaller than, the sum of available points')


    @classmethod
    def draft_to_staticfeedback_kwargs(cls, draftstring, configstring):
        #TODO: For now, 'grade' is just set to be points, but all info from configs and drafts is available here, so anything can be shown to the student.
        # might want to add grade-calculation like autograde in the config though..
        draft = json.loads(draftstring)
        config = json.loads(configstring)
        draftval = draft['values']
        confval = config['formValues']
        points = 0

        for i in xrange(0, len(draftval)):
            if confval[i][0]=='check':
                if draftval[i]:
                    points+=int(confval[i][1])

            elif confval[i][0] == 'number':
                points+=draftval[i]

        is_approved = False
        if points >= config['approvedLimit']:
            is_approved = True

        return dict(is_passing_grade=is_approved,
                    grade=points,
                    points=points,
                    rendered_view=markdown_full(draft['feedback']))

gradeeditor_registry.register(BasicForm)
