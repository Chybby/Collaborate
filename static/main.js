$(document).ready(function() {

  var courses = new Bloodhound({
    datumTokenizer: function(d) { return Bloodhound.tokenizers.whitespace(d.code); },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    limit: 10,
    local: [{"code": "COMP0011"}, {"code": "COMP1000"}, {"code": "COMP1400"}, {"code": "COMP1911"}, {"code": "COMP1917"}, {"code": "COMP1921"}, {"code": "COMP1927"}, {"code": "COMP2041"}, {"code": "COMP2111"}, {"code": "COMP2121"}, {"code": "COMP2911"}, {"code": "COMP2920"}, {"code": "COMP3121"}, {"code": "COMP3131"}, {"code": "COMP3141"}, {"code": "COMP3151"}, {"code": "COMP3152"}, {"code": "COMP3153"}, {"code": "COMP3161"}, {"code": "COMP3171"}, {"code": "COMP3211"}, {"code": "COMP3222"}, {"code": "COMP3231"}, {"code": "COMP3241"}, {"code": "COMP3311"}, {"code": "COMP3331"}, {"code": "COMP3411"}, {"code": "COMP3421"}, {"code": "COMP3431"}, {"code": "COMP3441"}, {"code": "COMP3511"}, {"code": "COMP3601"}, {"code": "COMP3711"}, {"code": "COMP3821"}, {"code": "COMP3891"}, {"code": "COMP3901"}, {"code": "COMP3902"}, {"code": "COMP4001"}, {"code": "COMP4121"}, {"code": "COMP4128"}, {"code": "COMP4141"}, {"code": "COMP4161"}, {"code": "COMP4181"}, {"code": "COMP4211"}, {"code": "COMP4314"}, {"code": "COMP4317"}, {"code": "COMP4335"}, {"code": "COMP4336"}, {"code": "COMP4411"}, {"code": "COMP4415"}, {"code": "COMP4416"}, {"code": "COMP4418"}, {"code": "COMP4431"}, {"code": "COMP4442"}, {"code": "COMP4511"}, {"code": "COMP4601"}, {"code": "COMP4904"}, {"code": "COMP4905"}, {"code": "COMP4906"}, {"code": "COMP4910"}, {"code": "COMP4911"}, {"code": "COMP4920"}, {"code": "COMP4930"}, {"code": "COMP4931"}, {"code": "COMP6714"}, {"code": "COMP6721"}, {"code": "COMP6731"}, {"code": "COMP6741"}, {"code": "COMP6752"}, {"code": "COMP6771"}, {"code": "COMP9009"}, {"code": "COMP9018"}, {"code": "COMP9020"}, {"code": "COMP9021"}, {"code": "COMP9024"}, {"code": "COMP9031"}, {"code": "COMP9032"}, {"code": "COMP9041"}, {"code": "COMP9101"}, {"code": "COMP9102"}, {"code": "COMP9116"}, {"code": "COMP9117"}, {"code": "COMP9151"}, {"code": "COMP9152"}, {"code": "COMP9153"}, {"code": "COMP9161"}, {"code": "COMP9171"}, {"code": "COMP9181"}, {"code": "COMP9201"}, {"code": "COMP9211"}, {"code": "COMP9222"}, {"code": "COMP9242"}, {"code": "COMP9243"}, {"code": "COMP9245"}, {"code": "COMP9283"}, {"code": "COMP9311"}, {"code": "COMP9314"}, {"code": "COMP9315"}, {"code": "COMP9317"}, {"code": "COMP9318"}, {"code": "COMP9319"}, {"code": "COMP9321"}, {"code": "COMP9322"}, {"code": "COMP9323"}, {"code": "COMP9331"}, {"code": "COMP9332"}, {"code": "COMP9333"}, {"code": "COMP9334"}, {"code": "COMP9335"}, {"code": "COMP9336"}, {"code": "COMP9414"}, {"code": "COMP9415"}, {"code": "COMP9416"}, {"code": "COMP9417"}, {"code": "COMP9431"}, {"code": "COMP9441"}, {"code": "COMP9444"}, {"code": "COMP9447"}, {"code": "COMP9511"}, {"code": "COMP9517"}, {"code": "COMP9519"}, {"code": "COMP9596"}, {"code": "COMP9801"}, {"code": "COMP9814"}, {"code": "COMP9844"}, {"code": "COMP9945"}] // hax 2 da max
  });

  courses.initialize();

  $('#course-search').typeahead(null, {
    name: 'courses',
    displayKey: 'code',
    source: courses.ttAdapter()
  });

  $('#course-search').keyup(function(event) {
    if (event.keyCode == 13) { //enter
      window.location = '/course/' + this.value;
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
