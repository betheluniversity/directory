$(document).ready(function () {
    $(".directory-form").submit(function(event) {
        /* stop form from submitting normally */
        event.preventDefault();

        /* get the action attribute from the <form action=""> element */
        var $form = $( this ),
          url = $form.attr('action');

        var $event_data = {
            // DROPDOWN OPTION
            // 'search_type': $('#search_type').val(),
            'search_type': $('#search_type input:radio:checked').val(),
            'first_name': $('#first_name').val(),
            'last_name': $('#last_name').val(),
            'username': $('#username').val(),
            'email': $('#email').val(),
            'department': $('#department').val(),
            'bu_id': $('#bu_id').val(),
            'view_ids': $('.view_ids').is(':checked') || 'false',
            'home': $('.home').is(':checked') || 'false',
            // 'group': $('.group').is(':checked') || 'false',
            'student': $('.student').is(':checked') || 'false',
            'faculty_or_staff': $('.faculty_or_staff').is(':checked') || 'false'
        };

        console.log(event);

        /* Send the data using post */
        $.post( url, $event_data ).done(function(data) {
            $('#results').html(data);
        });
    });

    $('#search_type').change(function(){
        var $search_type = $('#search_type input:radio:checked').val();

        // this is a quick way to make all fields hidden that aren't already hidden.
        $('.name_search:not(.d-none)').addClass('d-none');
        $('.username_search:not(.d-none)').addClass('d-none');
        $('.email_search:not(.d-none)').addClass('d-none');
        $('.dept_search:not(.d-none)').addClass('d-none');
        $('.id_search:not(.d-none)').addClass('d-none');

        // this is set up so the select value is equivalent of the class that we want to show.
        $("." + $search_type).removeClass('d-none');
    });
});
