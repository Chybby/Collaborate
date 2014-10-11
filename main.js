$(document).ready(function() {
    // Focus state for append/prepend inputs
    $('.input-group').on('focus', '.form-control', function () {
      $(this).closest('.input-group, .form-group').addClass('focus');
    }).on('blur', '.form-control', function () {
      $(this).closest('.input-group, .form-group').removeClass('focus');
    });

    var states = new Bloodhound({
      datumTokenizer: function(d) { return Bloodhound.tokenizers.whitespace(d.word); },
      queryTokenizer: Bloodhound.tokenizers.whitespace,
      limit: 4,
      local: [
        { word: "Alabama" },
        { word: "Alaska" },
        { word: "Arizona" },
        { word: "Arkansas" },
        { word: "California" },
        { word: "Colorado" }
      ]
    });

    states.initialize();

    $('#course-search').typeahead(null, {
      name: 'states',
      displayKey: 'word',
      source: states.ttAdapter()
    });
});
