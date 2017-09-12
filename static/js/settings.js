//-----------------------------------------------------------
/**
 * 调试配置，请只在这个地方进行设置，不要动其他代码
 */
var debug = true; // 是否是调试模式，注意：在上传代码的时候，要改为false
//-----------------------------------------------------------

//以下公用代码区域，使用范围非常广，请勿更改--------------------------------
//403 ajax 请求错误时artdialog提示
if (typeof(remote_static_url) == "undefined"){
	remote_static_url = 'http://t.open.oa.com/static_api/';
}
document.write(" <script lanague=\"javascript\" src=\""+remote_static_url+"artdialog/jquery.artDialog.js?skin=default\"> <\/script>");

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

/*
 * 打开登录窗口
 */
function open_login_dialog(src){
	login_html = '<div style="overflow: hidden;width: 490px;"><iframe name="iframe_401" scrolling="no" frameborder="0" src="'+src+'" style="width:490px;height: 460px;"></iframe></div>';
	art.dialog({
		id:"401_dialog",
		title: "登录",
		fixed: true,
		lock: true,
		padding: "0px 0px",
		content: login_html
	});
}

/*
 * 关闭登录框
 */
function close_login_dialog(){
	//art.dialog({id: '401_dialog'}).close();
	// 设置登录框的超时时间为1s，1s后自动关闭
	art.dialog({id: '401_dialog'}).time(1);
}
/*
 *  登录提示
 * 不在蓝鲸平台中，则跳转到蓝鲸平台中
 */
function jump_to_pt(app_code){
	var d_tips = "温馨提示：请在蓝鲸平台中使用该应用！<br>即将跳转至蓝鲸平台！"
	var tips =arguments[1]? arguments[1]:d_tips;
	var bk_url = window.location.host;
	// 当前应用的宣传链接
	if(app_code != ''){
		var jump_url =  'http://'+bk_url + "/?app=" + app_code;
	}else{
		var jump_url =  'http://'+bk_url + "/";
	}
	art.dialog({
		title: "温馨提示",
		width: 340,
		icon: 'warning',
		lock: true,
		content: tips,
		time: 2,
		close: function () {
			window.top.location = jump_url;
		}
	});
}
/**
 * ajax全局设置
 */
// 在这里对ajax请求做一些统一公用处理
$.ajaxSetup({
//	timeout: 8000,
	statusCode: {
	    401: function(xhr) {
	    	// 正式环境中判断是否在蓝鲸平台中打开
	    	var _src = xhr.responseText;
	    	// 判断返回的url是否正确
	    	var is_src  = _src.indexOf('http://');
	    	if(is_src != 0){
	    		var tips = "温馨提示：用户信息验证失败！<br>即将跳转至登录页面！"
    			jump_to_pt(app_code, tips);
	    	}else{
	    		// 判断是否是在蓝鲸平台中打开
	    		try{
	    			window.top.BLUEKING.corefunc.open_login_dialog(_src);
	    		}catch(err){
	    			open_login_dialog(_src);
	    		}
	    	}
	    },
	    402: function() {
	    	//@APP开发者: 请注意,如果某操作需要使用ajax请求敏感系统,务必要在包含该操作的页面的view函数上
	    	//					 加上@tof_check_session来登录敏感系统.
	    	//					(因为登录敏感需要页面重定向, 而ajax无法进行重定向操作)
	    	//这里是不应该出现的错误(ajax请求敏感系统前没有登录)
	    	alert("还没有登录到敏感系统, 请通过刷新当前页面来登录到敏感系统.\n" +
					  "如果刷新后依然无法登录, 请通知APP开发者进行改正(敏感系统的ajax请求不符合规范). ");
			return;
	    },
	    403: function(xhr) {
	    	// 主要用于敏感权限系统的无权限或验证出错的情况
	    	var _src = xhr.responseText;
	    	// 动态设置iframe的高度和宽度
	    	var body_width = $(document.body).width();
	    	var body_height = $(document.body).height();
	    	var frame_width = body_width < 570 ? body_width-40 : 570;
	    	var frame_height = body_height < 380 ? body_height-40: 380;
	    	ajax_content = '<iframe name="iframe_403" frameborder="0" src="'+_src+'" style="width:'+frame_width+'px;height:'+frame_height+'px;"></iframe>';
			art.dialog({
			    title: "提示",
			    lock: true,
			    content: ajax_content
			});
	    	return;
	    },
	    500: function(xhr, textStatus) {
	    	// 异常
	    	if(debug){
	    		alert("系统出现异常("+xhr.status+'):' + xhr.responseText);
	    	}
	    	else{
	    		alert("系统出现异常, 请记录下错误场景并与开发人员联系, 谢谢!");
	    	}
	    }
	}
});
/**
 * xssCheck 将用js渲染的html进行转义
 * @param str 需要转义的字符串
 * @param reg 需要转义的字符等，可选参数
*/
function xssCheck(str,reg){
    return str ? str.replace(reg || /[&<">'](?:(amp|lt|quot|gt|#39|nbsp|#\d+);)?/g, function (a, b) {
        if(b){
            return a;
        }else{
            return {
                '<':'&lt;',
                '&':'&amp;',
                '"':'&quot;',
                '>':'&gt;',
                "'":'&#39;',
            }[a]
        }
    }) : '';
}
