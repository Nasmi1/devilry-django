Ext.define('devilry_subjectadmin.view.passedpreviousperiod.PassedPreviousPeriodOverview' ,{
    extend: 'Ext.container.Container',
    alias: 'widget.passedpreviousperiodoverview',
    cls: 'devilry_subjectadmin_passedpreviousperiodoverview',
    requires: [
        'devilry_subjectadmin.view.passedpreviousperiod.SelectGroupsGrid',
        'devilry_subjectadmin.view.passedpreviousperiod.ConfirmGroupsGrid',
        'devilry_extjsextras.PrimaryButton',
        'devilry_extjsextras.AlertMessage'
    ],

    /**
     * @cfg {String} assignment_id (required)
     */

    // Internal attribute used for the width of the west-panel on all pages
    sideBarWidth: 250,

    initComponent: function() {
        Ext.apply(this, {
            padding: '20 40 20 40',
            layout: 'border',
            style: 'background: transparent !important;',

            items: [{
                xtype: 'box',
                region: 'north',
                height: 55,
                cls: 'bootstrap',
                html: [
                    '<h1 style="margin: 0; padding: 0;">',
                        gettext('Passed previously'),
                    '</h1>'
                    ].join('')
            }, {
                xtype: 'container',
                region: 'center',
                layout: 'card',
                itemId: 'cardContainer',
                items: [{
                    xtype: 'container',
                    itemId: 'pageOne',
                    layout: 'border',
                    style: 'background: transparent !important;',
                    items: [{
                        xtype: 'selectpassedpreviousgroupsgrid',
                        region: 'center',
                        fbar: [{
                            xtype: 'checkbox',
                            boxLabel: gettext('Show groups that Devilry believes should not be marked as previously passed?'),
                            itemId: 'showUnRecommendedCheckbox',
                            cls: 'showUnRecommendedCheckbox'
                        }, '->', {
                            xtype: 'button',
                            scale: 'large',
                            text: gettext('Next'),
                            disabled: true,
                            itemId: 'nextButton'
                        }]
                    }, {
                        xtype: 'box',
                        region: 'west',
                        width: this.sideBarWidth,
                        cls: 'bootstrap',
                        padding: '0 30 0 0',
                        html: [
                            '<p class="text-info">',
                                interpolate(gettext('Select one or more groups. Groups that we belive have passed this assignment before has been selected automatically, and they are marked with the name of the old %(period_term)s.'), {
                                        period_term: gettext('period')
                                    }, true),
                            '</p>',
                            '<p class="muted"><small>',
                                gettext('The search for previously passed students match the short name of old assignments against the short name of this assignment. Only groups with exactly one student in both the old and the current assignment is matched. You can find the short name of an assignment by looking at the breadcrumb in the header, or in the title of the Rename-section of "Dangerous actions" when visiting the assignment.'),
                            '</small></p>'
                        ].join('')
                    }]
                }, {
                    xtype: 'container',
                    itemId: 'pageTwo',
                    style: 'background: transparent !important;',
                    layout: 'border',
                    items: [{
                        xtype: 'box',
                        region: 'west',
                        width: this.sideBarWidth,
                        cls: 'bootstrap',
                        padding: '0 30 0 0',
                        html: [
                            '<p class="text-info">',
                                gettext('Make sure you really want to mark these groups as previously passed before saving.'),
                            '</p>',
                            '<p class="muted"><small>',
                                gettext('This will create a new delivery on each of the groups, mark the delivery as a placeholder for a previously approved delivery, and create a feedback with passing grade on the delivery.'),
                            '</small></p>'
                        ].join('')
                    }, {
                        xtype: 'confirmpassedpreviousgroupsgrid',
                        region: 'center',
                        fbar: [{
                            xtype: 'button',
                            text: gettext('Back'),
                            itemId: 'backButton'
                        }, '->', {
                            xtype: 'primarybutton',
                            text: gettext('Save'),
                            itemId: 'saveButton'
                        }]
                    }]
                }, {
                    itemId: 'unsupportedGradeEditor',
                    xtype: 'alertmessage',
                    type: 'error',
                    title: 'Unsupported grading system',
                    messagetpl: gettext('The passed previously functionality is not supported by the grading system configured on this assignment ({gradingsystem}).'),
                    messagedata: {
                        gradingsystem: gettext('Loading') + ' ...'
                    }
                }]
            }]
        });
        this.callParent(arguments);
    }
});