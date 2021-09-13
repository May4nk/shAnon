function getcsrfToken(name){
	let cookieVal = null;
	if(document.cookie && document.cookie != ''){
		const cook = document.cookie.split(';');
		for (let i = 0;i< cook.length ; i++){
			let val = cook[i].trim();
			if(val.substring(0 , name.length+1)===(name + '=')){
				cookieVal = decodeURIComponent(val.substring(name.length+1));
				break;
			}
		}
	}
	return cookieVal;
}
/*
(function($) {
    $.fn.clickToggle = function(func1, func2) {
        var funcs = [func1, func2];
        this.data('toggleclicked', 0);
        this.click(function() {
            var data = $(this).data();
            var tc = data.toggleclicked;
            $.proxy(funcs[tc], this)();
            data.toggleclicked = (tc + 1) % 2;
        });
        return this;
    };
}(jQuery));
*/
function pic(e,tag,input){
	var reader = new FileReader();
	reader.onload = function (){
		$(tag).attr('src',reader.result);
	}
	reader.readAsDataURL(input.files[0]);
}

$('.image_click').on('change',function(){
	pic(event,'#output_img',this);
});

$('.image_clk').on('change',function(){
	pic(event,'#cimg',this);
	pix_id=$(this).attr('id');
	src = $(this).val()
	srco = src.substring(12)
	$.ajax({
		type: 'POST',
		url: 'pix/',
		headers: {
		"X-CSRFToken": getcsrfToken('csrftoken'),
		},
		data: {
			pix_id: pix_id,
			src : srco,
		},
		'success': (data) => {
			if(data){
				location.reload();
			}
		}
	});	

});

$('.box41_icn').click(function(){
	like_id = $(this).attr('data');
	const csrftoken = getcsrfToken('csrftoken');
	$.ajax({
		type: 'POST',
		url: 'like/',
		headers: {
		"X-CSRFToken": csrftoken,
		},
		data: {
			post_id: like_id,
		//	csrfmiddlewaretoken: csrftoken,
		},
		'success': (data) => {
			if(data){
				location.reload();
			}
		}
	});	
});

$('.box42_icn').click(function(){
	like_id = $(this).attr('data');
	const csrftoken = getcsrfToken('csrftoken');
	$.ajax({
		type: 'POST',
		url: 'unlike/',
		headers: {
		"X-CSRFToken": csrftoken,
		},
		data: {
			post_id: like_id,
		//	csrfmiddlewaretoken: csrftoken,
		},
		'success': (data) => {
			if(data){
                	location.reload();
			}
		}
	});	
});


$('.but').click(function(){
	save_id = $(this).parent().siblings().children('#h').attr('data');
	$.ajax({
		type: 'POST',
		url: 'saved/',
		data:{
			post_id:save_id,
		},
		headers: {
			'X-CSRFToken' : getcsrfToken('csrftoken'),
		},

		success:(data)=>{
			location.reload();	
		},
	});
	
});

$('.but1').click(function(){
	save_id = $(this).parent().siblings().children('#h').attr('data');
	$.ajax({
		type: 'POST',
		url: 'unsaved/',
		data:{
			post_id:save_id,
		},
		headers: {
			'X-CSRFToken' : getcsrfToken('csrftoken'),
		},

		success:(data)=>{
			location.reload();
		},
	});
	
});

$('.border').click(function(e){
	like_id = $(this).attr('data');
	$.ajax({
		type: 'POST',
		url: 'cmnt/',
		data:{
			post_id:like_id,
			cmnt: $(this).siblings('#cmnt').val(),
		},
		headers: {
			'X-CSRFToken' : getcsrfToken('csrftoken'),
		},

		success:(data)=>{
			location.reload();
			$(this).siblings('#cmnt').val('');
		},
	});
});

$('.tabs').click(function(){
	id = $(this).html().trim();
	$(this).addClass('active');
	$('.tabs').not(this).removeClass('active');
	$('.tabcontent').css('display','none');
	$(`#${id}`).css('display','block');
});

$('#default').click();

$('.follow').click(function(){
	user_id = $(this).attr('id').trim();
	$.ajax({
		type: 'POST',
		url: 'follow/',
		headers:{
			'X-CSRFToken': getcsrfToken('csrftoken'),
		},
		data: {
			'user_id':user_id,	
		},
		success: function(){
			location.reload();
		},
	});
});


$('.following').click(function(){
	user_id = $(this).attr('id').trim();
	$.ajax({
		type: 'POST',
		url: 'unfollow/',
		headers:{
			'X-CSRFToken': getcsrfToken('csrftoken'),
		},
		data: {
			'user_id':user_id,	
		},
		success: function(){
			location.reload();
		},
	});
});

