var domain = window.location.host;
(function () {
    const debug = false;
    !debug && init();

    $('#addcard').on('click', function () {
        // window.location.href = 'regist.html'
        window.location.href = '/health/card';
    });
    debug &&
    buildcardlist([
        {
            name: '用户姓名',
            cardType: '2',
            idCard: '4401**********4225',
            qrCodeText: '2',
            phone1: '2'
        }
    ]);
})();

function init() {
    var cardlist = [];
    $.ajax({
        url: '/health/health_list/',
        type: 'get',
        dataType: 'json',
        success: function (resp) {
            console.log((resp));
            if (resp.retcode === 0) {
                cardlist = resp.cards;
                buildcardlist(cardlist);
            } else if (resp.retcode === 302) {
                window.location.href = resp.redirect_uri;
            }
        }
    });
    // var data = {"retcode":0,"retmsg":"","cards":[{"wechatCode":"7D773CE8301D18C8A78C1A4A5B17B028","0":"7D773CE8301D18C8A78C1A4A5B17B028","name":"\u5f20\u534e\u5a1f","1":"\u5f20\u534e\u5a1f","gender":"\u5973","2":"\u5973","nation":"\u6c49\u65cf","3":"\u6c49\u65cf","birthday":"1988-02-20","4":"1988-02-20","idCard":"3714**********6061","5":"371422198802206061","cardType":"0","6":"0","address":"\u798f\u5efa\u7701\u4e09\u660e\u5e02\u5efa\u5b81\u53bf\u4e0b\u574a\u88579\u53f7","7":"\u798f\u5efa\u7701\u4e09\u660e\u5e02\u5efa\u5b81\u53bf\u4e0b\u574a\u88579\u53f7","phid":"","8":"","phone1":"139******21","9":"13938084121","phone2":null,"10":null,"qrCodeText":"0001E5B8A28B9CB7CFA1DE92B0D5FDDAFB210FA1F644A5C1001558A1E13981A5:1","11":"0001E5B8A28B9CB7CFA1DE92B0D5FDDAFB210FA1F644A5C1001558A1E13981A5:1","patid":"","12":"","openid":"o4kcV1p532xwgt2NC4CEz42HgKK8","13":"o4kcV1p532xwgt2NC4CEz42HgKK8"}]}
    // buildcardlist(data.cards)

}

function buildcardlist(list) {
    var length = 0;
    var listhtml = '';
    console.log(list.length)
    if (list.length >= 5) {
        length = 5;
        $('#addcard').hide();
    } else {
        length = list.length;

        $('#tips').html('您还可以添加' + (5 - list.length) + '张健康卡');
    }

    if (length === 0) {
        $('#cardlist').css('background', 'transparent');
        // let binded = getCookie('bindhealthcard')
        // if (!binded) {
        // 	window.location.href = 'https://healthcarddemo.tengmed.com/index.php?c=healthcard&a=authhealthCode'
        // 	setCookie('bindhealthcard', true)
        // }

        listhtml = '<div class="emptycard"><img src="/static/health/img/nocard.png"/><p>暂无健康卡</p></div>';
    } else {
        for (var i = 0; i < length; i++) {
            let name = '';
            if (list[i].name.length == 2) {
              name = list[i].name.replace(/^(.).$/g, "$1*");
            } else {
              name = list[i].name.replace(/^(.).+(.)$/g, "$1*$2");
            }
            // var name = list[i].name.replace(/^(.).+(.)$/g, "$1*$2");
            const phone = list[i].phone.replace(/^(\d{3})\d{4}(\d+)/, "$1****$2");
            const card = list[i].idCard.replace(/^(.{4})(?:\d+)(.{4})$/, "$1**********$2");
            listhtml =
                listhtml +
                '<a href="/health/personal/' + list[i].id + '" class="card-face-container">' +
                `<img class="card-bg" src="/static/health/img/cardnewbg.png" alt="" />
                <div class="card-top-info">
                    <div class="card-top-org">广东省卫生健康委员会</div>
                    <div class="card-top-title">
                        <img src="/static/health/img/icon2.png" alt="" />
                        <span>电子健康卡</span>
                    </div>
                </div>
                <div class="card-detail-info">
                    <div class="card-user-info">
                        <span class="card-user-name">${name}</span>
                        <span class="card-user-id">${card}</span>
                    </div>
                    <div class="card-qrcode">
                        <img class="card-qrcode-logo" src="/static/health/img/logo_.png" alt="" />
                        <div class="qrcode qr${i}" ></div>
                    </div>
                </div>\
                <div class="card-footer">\
                    中华人民共和国国家卫生健康委员会监制\
                </div>` +
                '</a>';
        }
    }
    $('#cardlist').html(listhtml);
    for (var i = 0; i < length; i++) {
        jQuery('.qr' + i).qrcode({
            width: '200', //二维码的宽度
            height: '200',
            render: 'canvas',
            text: list[i].qrCodeText,
            background: '#ffffff', //二维码的后景色
            foreground: '#000000', //二维码的前景色
            src: '/static/health/img/logo_.png' //二维码中间的图片
        });
    }

}

//获取cookie
function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + '=');
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(';', c_start);
            if (c_end == -1) {
                c_end = document.cookie.length;
            }
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return '';
}

//获取url参数
function getQueryString(name) {
    var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)'); // 匹配目标参数
    var result = window.location.search.substr(1).match(reg); // 对querystring匹配目标参数
    if (result != null) {
        return decodeURIComponent(result[2]);
    } else {
        return null;
    }
}

//设置cookie
function setCookie(c_name, value, expiredays) {
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + expiredays);
    document.cookie = c_name + '=' + escape(value) + (expiredays == null ? '' : ';expires=' + exdate.toGMTString());
}
