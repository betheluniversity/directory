$(document).ready(function () {
    $(".directory-form").submit(function(event) {
        /* stop form from submitting normally */
        event.preventDefault();

        /* get the action attribute from the <form action=""> element */
        var $form = $( this ),
          url = $form.attr( 'action' );

        var $event_data = {
            'first_name': $('#first_name').val(),
            'last_name': $('#last_name').val(),
            'username': $('#username').val(),
            'email': $('#email').val(),
            'department': $('#department').val(),
            'bu_id': $('#bu_id').val(),
            'home': $form.find('.home').is(':checked'),
            'group': $form.find('.group').is(':checked'),
            'student': $form.find('.student').is(':checked'),
            'faculty': $form.find('.faculty').is(':checked')
        };

        /* Send the data using post */
        $.post( url, $event_data ).done(function( data ) {
            $('#results').html(data);
        });
    });
});
