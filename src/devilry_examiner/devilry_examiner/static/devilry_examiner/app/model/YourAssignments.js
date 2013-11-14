// Generated by CoffeeScript 1.6.3
(function() {
  Ext.define('devilry_examiner.model.YourAssignments', {
    extend: 'Ext.data.Model',
    fields: [
      {
        name: 'results',
        type: 'auto'
      }
    ],
    proxy: {
      type: 'ajax',
      url: 'assignments.json',
      headers: {
        'Accept': 'application/json'
      },
      reader: {
        type: 'json'
      }
    }
  });

}).call(this);
