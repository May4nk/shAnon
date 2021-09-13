/*------chat---------*/
let loc = window.location;
let ws = 'ws://';
if(loc.protocol === 'https'){
	ws = 'wss://';
}
let endpoint = ws + loc.hostname + ':' + loc.port + loc.pathname;

let id= $('.box6_title').children('a').attr('data');

let socket = new WebSocket(endpoint);

socket.onopen = async function(e){
	console.log('open',e)
	$('.chat_in').keyup(function(i){
		if(i.keyCode == '13'){
			if(i.target.value === ''){
				return False
			}
			let send_to;
			if (id == 1){
				send_to=2
			}
			else{
				send_to=1
			}
			let data = {
				'message': i.target.value,
				'send_by': id,
				'send_to': send_to,
			}
			data = JSON.stringify(data)
			socket.send(data)
			$(this).val('');
		}
	});


}
 
socket.onmessage = async function(e){
	console.log('message',e)
	let data=JSON.parse(e.data);
	let message = data['message'];
	let sent_by_id = data['send_by']
	myfunc(message,sent_by_id);
}

socket.onerror = async function(e){
	console.log('error',e)
}

socket.onclose = async function(e){
	console.log('close',e)
}

function myfunc(i,sent_by_id){

	let message = `
		<div class='row'>
			<div class='sender'>
			    ${i}
			</div>
		</div>
	`;
	$('.ove').append($(message));
	$('.ove').animate({
		scrollTop: $(document).height(),
	},100);
};
