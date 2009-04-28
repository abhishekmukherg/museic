$(function(){
        $('#id_date_of_birth').addClass('hide');
        $('#id_date_of_birth').before('<div class="calendar"></div>');
        var curset_date = $.datepicker.parseDate('yy-mm-dd',
            $('#id_date_of_birth').val());
        $('.calendar').datepicker({ altField: '#id_date_of_birth',
           altFormat: 'yy-mm-dd',
           dateFormat: 'yy-mm-dd',
           defaultDate: curset_date,
	   yearRange: '1900:2009',
          onSelect: updateDate });
        function updateDate(dateStr) {
            $('#id_date_of_birth').val(dateStr);
        }
});

