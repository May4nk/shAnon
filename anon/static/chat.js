let loc = window.location
let strt = 'ws://';
if(loc.protocol === 'https'){
	strt = 'wss://';
}

const curr_id= $('.box6_title').children('a').attr('data');

let sconnect = strt + loc.host + loc.pathname;

let socket = new WebSocket(sconnect);

socket.onopen = async function(e){
	console.log('open',e);
	$('.chat_in').keyup(function(i){
		if(i.keyCode == '13'){
			let send_to = get_act_usr();
			let data = {
				'message': i.target.value,
				'sent_by': curr_id,
				'sent_to': send_to
			}
			data = JSON.stringify(data);
			socket.send(data);
			$(this).val('');
		}
	});
}

socket.onmessage = async function(e){
	console.log('message',e);
	let data = JSON.parse(e.data);
	let message = data['message'];
	let sent_by = data['sent_by'];
	newmsg(message,sent_by);
}

socket.onerror = async function(e){
	console.log('error',e);
}

socket.onclose = async function(e){
	console.log('close',e);
}

function newmsg(msg,send_by){
	
	if($.trim(msg)===''){
		return false;
	}
	
	let message;
	if(send_by==curr_id){
		message = 
			`
		    <div class='row'>
			    <div class='sender'>${msg}</div>
		    </div>	
		`;
	}else{
		message = 
			`
		    <div class='row'>
			    <div class='receiver'>${msg}</div>
		    </div>	
		`;
	}	
	$(`#ove${get_act_usr()}`).append($(message));
	$('.ove').animate({
		scrollTop: $(document).height()
	},100);
}

function get_act_usr(){
	let ouser = $('.active').attr('id');
	ouser = $.trim(ouser);
	return ouser;
}

$('#modal1').click(function(){
	$('#modalx').show();
});

$('.follow_names').on("click", function() {
	$.ajax({
		type: 'POST',
		url: '',
		headers:{
			'X-CSRFToken': getcsrfToken('csrftoken'),
		},
		data: {
			'value':$(this).attr('data-id'),	
		},
		success: function(){
			location.reload();
		},
	});
});


$('.close').click(function(){
	$('.modal').hide();
});

$('.chatter_box').click(function(){
	$(this).addClass('active');
	$('.chatter_box').not(this).removeClass('active');
	let chat_id = $(this).attr('id');
	$('.is_active').removeClass('is_active');
	$('.box_chat[id="' +chat_id +'"]').addClass('is_active');
});

