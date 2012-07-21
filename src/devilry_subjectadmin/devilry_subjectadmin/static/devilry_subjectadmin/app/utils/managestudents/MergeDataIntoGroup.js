Ext.define('devilry_subjectadmin.utils.managestudents.MergeDataIntoGroup', {
    singleton: true,

    requires: [
        'devilry_subjectadmin.utils.Array'
    ],

    /**
     * Merge tags into groupRecord.
     *
     * @param {devilry_subjectadmin.model.Group} [groupRecord] Group record.
     * @param {[String]} [sourceTags] Array of tags. Each item is a string.
     * @param {Boolean} [doNotDeleteTags=false] Set this to ``true`` to append to existing tags.
     */
    mergeTags: function(groupRecord, sourceTags, doNotDeleteTags) {
        var tags = [];
        var currentTags = groupRecord.get('tags');
        devilry_subjectadmin.utils.Array.mergeIntoArray({
            destinationArray: currentTags,
            sourceArray: sourceTags,
            isEqual: function(tagObj, sourceTagString) {
                return tagObj.tag == sourceTagString;
            },
            onMatch: function(tagObj) {
                tags.push(tagObj);
            },
            onNoMatch: function(tagObj) {
                if(doNotDeleteTags) {
                    tags.push(tagObj);
                }
            },
            onAdd: function(sourceTagString) {
                tags.push({
                    tag: sourceTagString
                });
            }
        });
        groupRecord.set('tags', tags);
    },


    /**
     * Merge examiners into groupRecord.
     *
     * @param {devilry_subjectadmin.model.Group} [groupRecord] Group record.
     * @param {[devilry_subjectadmin.model.RelatedExaminerRo]} [userRecords]
     *      Array of user-records to merge into groupRecord. The only real requirement is
     *      that the record has an ID field, which contains a valid user-id.
     * @param {Boolean} [doNotDeleteUsers=false] Set this to ``true`` to append to existing examiners.
     * */
    mergeExaminers: function(groupRecord, userRecords, doNotDeleteUsers) {
        var examiners = [];
        var currentExaminers = groupRecord.get('examiners');
        devilry_subjectadmin.utils.Array.mergeIntoArray({
            destinationArray: currentExaminers,
            sourceArray: userRecords,
            isEqual: function(examiner, userRecord) {
                return examiner.user.id == userRecord.get('id');
            },
            onMatch: function(examiner) {
                examiners.push(examiner);
            },
            onNoMatch: function(examiner) {
                if(doNotDeleteUsers) {
                    examiners.push(examiner);
                }
            },
            onAdd: function(userRecord) {
                examiners.push({
                    user: {id: userRecord.get('id')}
                });
            }
        });
        groupRecord.set('examiners', examiners);
    },


    /**
     * Remove examiners from groupRecord.
     *
     * @param {Object} [config] Arguments. See below.
     * @param {devilry_subjectadmin.model.Group} [config.groupRecord] Group record.
     * @param {[devilry_subjectadmin.model.RelatedExaminerRo]} [config.userRecords]
     *      Array of user-records to remove from groupRecord. The only real
     *      requirement is that the record has an ID field, which contains a
     *      valid user-id.
     * @param {Function} [config.getUserId]
     *      Callback that takes a userRecord (on item in userRecords) and
     *      returns a userID.
     * */
    removeExaminers: function(config) {
        var examiners = [];
        var currentExaminers = config.groupRecord.get('examiners');
        devilry_subjectadmin.utils.Array.mergeIntoArray({
            destinationArray: currentExaminers,
            sourceArray: config.userRecords,
            isEqual: function(examiner, userRecord) {
                var userId = config.getUserId(userRecord);
                return examiner.user.id == userId;
            },
            onMatch: function(examiner) {
                // We do not include matches, which means they are deleted
                // since they are not included in the new examiners array
            },
            onNoMatch: function(examiner) {
                examiners.push(examiner);
            },
            onAdd: function(userRecord) {
                // Ignore any examiners not already in record
            }
        });
        config.groupRecord.set('examiners', examiners);
    }
});
