var clientId = "28b5ac55dadb221";
var overlayColor = '#2E0927';

$(document).ready(function() {
	$('#shutter').click(function() {
		$('#video').addClass('flash');
		
		setTimeout(function() {
			$('#video').removeClass('flash');
		}, 300);

		upload();
	});

	$('.overlay-buttons').on('click', function(e) {
		console.log(e.target.dataset.color);
		setOverlay(e.target.dataset.color);
	})
})

function setOverlay(color) {
	$('.overlay').css('background', color);
	overlayColor = color;
}

function upload(){
	var image = $('#video')[0];

	var canvas = document.createElement("canvas");
	    canvas.width = 640;
	    canvas.height = 240;
	var ctx = canvas.getContext("2d");
    ctx.drawImage(image, 0, 0);

    try {
        var img = canvas.toDataURL('image/jpeg', 0.9).split(',')[1];
    } catch(e) {
        var img = canvas.toDataURL().split(',')[1];
    }
    // upload to imgur using jquery/CORS
    // https://developer.mozilla.org/En/HTTP_access_control
    $.ajax({
    	method: 'POST',
        url: 'https://api.imgur.com/3/image',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("Authorization", "Client-ID " + clientId);
        },
        data: {
        	image: img,
            type: 'base64',
            name: 'foobar.jpg',
            title: 'test title',
            caption: 'test caption',
        }
    }).success(function(data) {
    	console.log(data);
        // w.location.href = data.data.link;
        var url = data.data.link;
        post(data.data.link, "Foobar");
    }).error(function() {
        alert('Could not reach api.imgur.com. Sorry :(');
    });
}

function post(url, submitter) {
	data = {image: {
		color: overlayColor,
		url: url
	}}
	$.ajax({
		method: 'POST',
		url: 'https://cryptic-basin-4493.herokuapp.com',
		// url: 'http://localhost:3000',
		contentType:"application/json; charset=utf-8",
		data: JSON.stringify(data)
	}).success(function(data) {
    	console.log(data);
    }).error(function() {
        alert('Could not reach cryptic-basin-4493.herokuapp.com');
    });
}