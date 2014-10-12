$(document).ready(function() {

  var courses = new Bloodhound({
    datumTokenizer: function(d) { return Bloodhound.tokenizers.whitespace('code'); },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    limit: 10,
    prefetch: {
      url: '',
      filter: function(list) {
        return $.map(list, function(course) { return { code: course }; });
      }
    }
  });

  courses.initialize();

  $('#course-search').typeahead(null, {
    name: 'courses',
    displayKey: 'code',
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
    var i
    for (i=0; parent.children()[i] != this; i++) {
      $(parent.children()[i]).css('color', '#E74C3C');
    }
    $(this).css('color', '#E74C3C');
    for (i++; i < parent.children().length; i++) {
      $(parent.children()[i]).css('color', '#34495E');
    }
  });
});
