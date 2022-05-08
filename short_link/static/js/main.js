
$('#createShortLink').on('click', function(){
    var longurl = $('#longUrl').val();
    $.ajax({
            url: URL + "encode",
            type: "POST",
            data: {
                url: longurl,
            },
            headers: { "X-CSRFToken": getCookie("csrftoken")},
            success:function(data){
                $('#shortLinkDisplay').text(data.url);
                $('#shortLinkDisplay').attr('href', longurl);
                $('#linklabel').text('Shortened Link: ')
                $('#statistics').text('Statistics');
                $('#statistics').attr('href', URL + "statistics");
                $('#statistics').addClass('btn btn-dark')
            },
            error: function(xhr, txtStatus, errorThrown){
                $('#shortLinkDisplay').text('Error: Unexpected error while retrieveing data.');
            }
    });
});

$('#shortLinkDisplay').on('click', function(){
    var link = $(this).text();
    $.ajax({
            url: URL + "count",
            type: "POST",
            data: {
                url: link,
            },
            headers: { "X-CSRFToken": getCookie("csrftoken")},
            success:function(data){
                if (Object.keys(data)[0] == "error") {
                    $('#showerror').text(data.error);
                }
            },
            error: function(xhr, txtStatus, errorThrown){
                $('#showerror').text('Error: Unexpected Error while updating click count.');
            }
    });
});

$('.deleteLink').on('click', function(){
    var link = $(this).attr('link');
    $.ajax({
            url: URL + "delete",
            type: "POST",
            data: {
                url: link,
            },
            headers: { "X-CSRFToken": getCookie("csrftoken")},
            success:function(data){
                if (Object.keys(data)[0] == "success") {
                    var rowId = 'row' + link.split(PREURL+'/')[1];
                    $('#msgbox').text(data.success);
                    $('.'+rowId).remove();
                } else {
                    $('#msgbox').text(data.error);
                }
            },
            error: function(xhr, txtStatus, errorThrown){
                $('#msgbox').text('Error: Unexpected Error while deleting the link.');
            }
    });
});

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}