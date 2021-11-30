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


$('.pr_title').hover(function(){
	let name = $(this).children('div').attr('data-name')
	let username = $(this).children('div').attr('data')
	let follower = $(this).children('div').attr('data-follower')
	let following = $(this).children('div').attr('data-following')
	let post = $(this).children('div').attr('data-post')
        $('<div class="profile_modal"></div>')
        .html(
    "<div class='row'>\n"+
        "<div class='box5_dot'>\n"+
        "</div>\n"+
	    "<div class='pm_text'>\n"+
	        "<a class='pm_text1' href=''>"+username+"</a>\n"+
	        "<div class='pm_text2'>"+name+"</div>\n"+
	    "</div>\n"+
    "</div>\n"+
    "<hr class='white'>\n"+
    "<div class='row pm_follow'>\n"+
        "<div class='center'>\n"+
	    "<div class='col s12'>\n"+
		 "<span class='col s4'>"+post+"</span>\n"+
		 "<span class='col s4'>"+following+"</span>\n"+
		 "<span class='col s4'>"+follower+"</span>\n"+
	    "</div>\n"+
	"</div>\n"+
        "<div class='center'>\n"+
	    "<div class='col s12'>\n"+
	   	 "<span class='col s4'>post</span>\n"+
		 "<span class='col s4'>following</span>\n"+
		 "<span class='col s4'>follower</span>\n"+
	    "</div>\n"+
	"</div>\n"+
    "</div>\n"+
    "</div>"
	)
        .appendTo('body')
        .fadeIn('slow');
}, function() {
        $('.profile_modal').remove();
}).mousemove(function(e) {
        var mousex = e.pageX + 20; 
        var mousey = e.pageY + 10; 
        $('.profile_modal')
        .css({ top: mousey, left: mousex })

});

$('.profile_status').one('click',function(e){
	let a = $(this).html()
	$(this).append(
	"<input id='status_input' type='text' maxlength='150' placeholder='"+a.trim()+"'/>"
	)
	$('#status_input').keyup(function(e){
		if( e.keyCode == '13'){
		      
		      $.ajax({
			      type: 'POST',
			      url: '#',
			      headers: {
				      "X-CSRFToken": getcsrfToken('csrftoken'),
			      },
			      data: {
				      stat : $('#status_input').val(),
			      },
			      'success': (data) => {
				      if(data){
					      location.reload();
				      }
			      }
		      }); 
		
	}
	})

})

$('.dele').click(function(){
	let delete_id = $(this).parent('div').attr('data-id')
	$.ajax({
	      type: 'POST',
	      url: 'delete/',
	      headers: {
		      "X-CSRFToken": getcsrfToken('csrftoken'),
	      },
	      data: {
		      delete_id: delete_id,
	      },
	      'success': (data) => {
		      if(data){
			      location.reload();
		      }
	      }
        }); 
});

$('#fing').click(function (){
    $('#modalfing').show();
});

$('.modalcross').click(function (){
    $('#modalfing').hide();
})

$('#fer').click(function (){
    $('#modalfer').show();
});

$('.modalcros').click(function (){
    $('#modalfer').hide();
})
