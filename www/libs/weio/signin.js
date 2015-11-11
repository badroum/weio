$( document ).ready(function() {
    // Get country list
    $.getJSON('data/countries.json', function(data) {
            var confFile = data;
            //console.log(confFile[0][1]);

            $("#countries").empty();
            for (var i=0; i<confFile.length; i++) {
                $("#countries").append('<option value="'+confFile[i][1]+'">'+confFile[i][0]+'</option>');
            }
    });

    // Get timezone list
    $.getJSON('data/timezones.json', function(data) {
            var confFile = data;

            $("#timezones").empty();
            for (var i=0; i<confFile.length; i++) {
                var value2 = '';
                var value3 = '';
                if(confFile[i].value2){
                    value2 =  ','+confFile[i].value2;
                }
                if(confFile[i].value3){
                    value3 = ','+confFile[i].value3;
                }
                $("#timezones").append('<option value="'
                        +confFile[i].value1+value2+value3+'">'
                        +confFile[i].region+' / '+confFile[i].city+'</option>');
            }

    });

// Inform user about timezone (changes will be applayed after system reboot) when they change selectbox
$('#timezones').on('change', function() {
   $("#timezone-msg").show();
});


});

$(function () { $("input,select,textarea").not("[type=submit]").jqBootstrapValidation(); } );
