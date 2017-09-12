if (typeof(remote_static_url) == "undefined"){
	remote_static_url = 'http://mt.bk.tencent.com/static_api/';
}
//csrftoken处理js
function choose_csrftoken_by_jquery(){
	var jquery_version = $().jquery;
	var current_version = jquery_version.split('.');
	var compare_version = [1, 10, 0];
	var result = true;
	for(var i = 0; i < 3 && result; i++){
		if(parseInt(current_version[i]) < compare_version[i]){
			result = false;
		}else if(parseInt(current_version[i]) > compare_version[i]){
			break;
		}
	}
	//大于或等于1.10.0
	if(result){
		document.write(" <script lanague=\"javascript\" src=\""+remote_static_url+"csrftoken_v3.js\"> <\/script>");
	}
	else{
		document.write(" <script lanague=\"javascript\" src=\""+remote_static_url+"csrftoken.js\"> <\/script>");
	}
}
choose_csrftoken_by_jquery();