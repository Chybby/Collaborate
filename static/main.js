$(document).ready(function() {

  var courses = new Bloodhound({
    datumTokenizer: function(d) { return Bloodhound.tokenizers.whitespace(d.course_code); },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    limit: 10,
    local: [
      { course_code: "COMP1917" },
      { course_code: "COMP1927" },
      { course_code: "COMP1911" },
      { course_code: "COMP2041" },
      { course_code: "COMP3891" },
      { course_code: "COMP2121" }
    ]
  });

  courses.initialize();

  $('#course-search').typeahead(null, {
    name: 'courses',
    displayKey: 'course_code',
    source: courses.ttAdapter()
  });

  $('#course-search').keyup(function(event) {
    if (event.keyCode == 13) { //enter
      console.log(this.value);
      $('#search-form').submit();
    }
  });

  $('div.star-rating button').click(function() {
    var parent = $(this.parentNode);
    for (var i=0; parent.children()[i] != this; i++) {
      parent.children()[i];
    }
  });
});
