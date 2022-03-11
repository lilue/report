// toast弹框函数，text为提示信息，type为操作反馈类型，是成功，失败还是提示...
function showToast(text,type) {
	if(!$('#weui-toast').length) {
		$('.container').append('<div id="weui-toast"><div class="weui-mask_transparent"></div><div class="weui-toast"><i class="weui-icon-'+type+'" weui-icon_toast"></i><p class="weui-toast__content" id="weui-toast-msg"></p></div></div>');
	}else {
		$('#weui-toast').remove();
		$('.container').append('<div id="weui-toast"><div class="weui-mask_transparent"></div><div class="weui-toast"><i class="weui-icon-'+type+'" weui-icon_toast"></i><p class="weui-toast__content" id="weui-toast-msg"></p></div></div>');
	};
	var $weui_toast = $('#weui-toast');
	var $weui_toast_msg = $('#weui-toast-msg');
	$weui_toast_msg.text(text);
	$weui_toast.fadeIn(100);
	setTimeout(function () {
		$weui_toast.fadeOut(100);
	}, 2000);
}
//toptip函数,text为提示信息
function showToptips(text) {
	if(!$('#weui-toptips').length) {
		$('.container').append('<div class="weui-toptips weui-toptips_warn" id="weui-toptips"></div>');
	}else {
		$('#weui-toptips').remove();
		$('.container').append('<div class="weui-toptips weui-toptips_warn" id="weui-toptips"></div>');
	}
	var $toolTips = $('#weui-toptips');
	$toolTips.text(text)
	$toolTips.fadeIn(200);
	setTimeout(function () {
		$toolTips.fadeOut(100);
	}, 2000);
}