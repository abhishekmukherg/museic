$(document).ready(function() {
    debug = true;

    $('div.comment-form form').submit(function() {
        $('div.comment-error').remove();

        comment = $('#id_comment').val();
        content_type = $('#id_content_type').val();
        object_pk = $('#id_object_pk').val();
        timestamp = $('#id_timestamp').val();
        security_hash = $('#id_security_hash').val();
        honeypot = $('#id_honeypot').val();

        $.post('/ajax/comment/post/', {
            comment: comment,
            content_type: content_type,
            object_pk: object_pk,
            timestamp: timestamp,
            security_hash: security_hash,
            honeypot: honeypot,
        }, function(data) {
            if (data.status == "success") {
                $('input.submit_post').attr('disabled', 'disabled');

                if ($('div#comments').children().length == 0) {
                    $('div#comments').prepend(
                        '<h2 class="comment-hd">1 comment so far:</h2>'
                    )
                }

                comment_html = '<div class="comment" style="display: none;">' +
                    '<div class="metadata"><h2><a href="' + data.url + '">' +
		    data.name + '</a></h2> opened his big mouth on ' + data.uday
		    + data.day + '</abbr></div>' + data.comment + '</div>';

                $('#comments').append(comment_html);
                $('div.comment:last').show('slow');

                $('.comment-form').hide()
                    .html('<p class="comment-thanks">Comment successfully' +
                            ' posted.</p>')
                    .show(2000);
            } else if (data.status == 'debug') {
                if (debug) {
                    $('div.comment.form').before('<div class="comment-error">' +
                                data.error + '</div>');
                } else {
                    $('div.comment-form').before('<div class="comment-error">' +
                        'There has been an internal error with the server. ' +
                        'Please contact a site administrator.</div>');
                }
            } else {
                $('div.comment-form').before('<div class="comment-error">' +
                    data.error + '</div>');
            }

        }, "json");


        return false;
    });
});

