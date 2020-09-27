var domain = window.location.host;
(function () {
    var cardTypeObj = {
        '10': '就诊卡',
        '11': '健康卡',
        '99': '其他法定有效证件',
        '01': '身份证号',
        '02': '居民户口簿',
        '03': '护照',
        '04': '军官证',
        '05': '驾驶证',
        '06': '港澳居民来往内地通行证',
        '07': '台湾居民来往内地通行证',
        '08': '出生医学证明',
        '09': '医保卡'
    };
    init(cardTypeObj);
    $('#openpopwindow').click(function () {
        $('.mask').show();
    });
    $('#cancel-btn').click(function () {
        $('.mask').hide();
    });
    $('#unbing-btn').click(function () {
        // 解绑操作
        const idx = $("#unbing-btn").data("id");
        $.ajax({
            url: '/health/untie/',
            data: {
                id: idx,
            },
            dataType: 'json',
            type: 'post',
            success: function (res) {
                if (res.retcode === 0) {
                    window.location.href = '/health/';
                } else {
                    // alert(res.retmsg);
                }
            }
        });
    });
    $('#entercard').click(function () {
        console.log('进入卡包')
        window.location.href = '/health/';
        // $.ajax({
        //     url: 'https://healthcarddemo.tengmed.com/index.php?c=healthcard&a=getOrderIdByOutAppId',
        //     data: {
        //         qrCodeText: getQueryString('qrCodeText')
        //     },
        //     dataType: 'json',
        //     type: 'post',
        //     success: function(res) {
        //         if (res.retcode === 0) {
        //             window.location.href =
        //                 'https://health.tengmed.com/open/takeMsCard?order_id=' +
        //                 res.orderId +
        //                 '&redirect_uri=' +
        //                 encodeURIComponent('https://healthcarddemo.tengmed.com/healthcard/list.html');
        //         }
        //     }
        // });
    });
})();

function init(cardTypeObj) {
    // var name = getQueryString('name') || '';
    // var idCard = getQueryString('idCard') || '*****';
    // var qrCodeText = getQueryString('qrCodeText') || '';
    // var phone = getQueryString('phone') || '';
    // var cardType = getQueryString('cardType') || 1;
    // var verify = getQueryString('verify') || false;
    // cardType = parseInt(cardType) > 9 ? cardType.toString() : '0' + cardType;

    // if (cardType !== '01') {
    //     $('.idcard-link').css('display', 'block');
    //     $('#idcard').css('display', 'none');
    // }
    const tempPhone = phone.replace(/^(\d{3})\d{4}(\d+)/, "$1****$2");
    // var tempName = name.replace(/^(.).+(.)$/g, "$1*$2");
    let tempName = '';
    if (name.length == 2) {
        tempName = name.replace(/^(.).$/g, "$1*");
    } else {
        tempName = name.replace(/^(.).+(.)$/g, "$1*$2");
    }
    const tempCard = idCard.replace(/^(.{4})(?:\d+)(.{4})$/, "$1**********$2");
    $('#name').html(tempName);
    $('#idcard').html(tempCard);
    $('#phone').html(tempPhone);
    $('#idcard')
        .prev()
        .html(cardTypeObj['01']);
    jQuery('.qrcode').qrcode({
        width: '200', //二维码的宽度
        height: '200',
        render: 'canvas',
        text: qrCodeText,
        background: '#ffffff', //二维码的后景色
        foreground: '#000000', //二维码的前景色
        src: '/static/health/img/logo_.png' //二维码中间的图片
    });

    $("#imgcode").JsBarcode(medical, {
        width: 2,
        height: 35,
    });


    // if (verify) {
    //     weui.toast('实名认证成功', {
    //         duration: 2000,
    //         className: 'verify-toast'
    //     });
    // }
}
