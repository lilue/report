(function() {
    // $.ajax({
    //     url: '/api/config',
    //     data: {
    //         url: window.location.href
    //     },
    //     beforeSend: function (xhr, settings) {
    //         xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    //     },
    //     dataType: 'json',
    //     type: 'post',
    //     success: function(res) {
    //         if (res.retcode === 0) {
    //             wx.config({
    //                 debug: false,
    //                 appId: res.data.appId,
    //                 timestamp: res.data.timestamp,
    //                 nonceStr: res.data.nonceStr,
    //                 signature: res.data.signature,
    //                 jsApiList: ['config', 'chooseImage', 'uploadImage', 'getLocalImgData']
    //             });
    //         }
    //     }
    // });

    wx.ready(function() {
        $('.upload-idcard').on('click', function(e) {
            e.preventDefault();
            wx.chooseImage({
                count: 1,
                sizeType: ['original', 'compressed'],
                sourceType: ['album', 'camera'],
                success: function(resp) {
                    $('.upload-image').attr('src', resp.localIds[0]);
                    $('.loading-mask').addClass('show');
                    wx.getLocalImgData({
                        localId: resp.localIds[0],
                        success: function(res) {
                            var localData = res.localData;
                            localData = localData.substr(localData.indexOf('base64,') + 7)
                            $('.loading-mask').addClass('show');
                            $.ajax({
                                url: '/api/ocr',
                                data: { img: localData },
                                dataType: 'json',
                                type: 'post',
                                success: function(res) {
                                    $('.loading-mask').removeClass('show');
                                    if (res.retcode === 0) {
                                        console.log(res.cardInfo)
                                        $('.input-block .name').val(res.cardInfo.name);
                                        $('.input-block .idCard').val(res.cardInfo.id);
                                        $('.input-block .nation').val(res.cardInfo.nation);
                                        $('.input-block .address-detail').val(res.cardInfo.address);
                                        checkInput('.input-tab');
                                        $('.next-btn').removeAttr('disabled');
                                    } else if (res.retcode === 302) {
                                        window.location.href = res.redirect_uri;
                                    } else {
                                        // alert(res.retmsg)
                                        $('#ocrfail-alert').addClass('show');
                                    }
                                }
                            });
                        }
                    });
                }
            });
        });
    });

    initPickder();
    $('#form-phone-verify').css('display', 'block');

    $('#confirm-btn').click(function() {
        $('#ocrfail-alert').removeClass('show');
    });

    $('.valid-btn').click(function() {
        var phone = $('.phone').val();
        if (!/^1\d{10}$/.test(phone)) {
            return weui.topTips('手机号格式错误');
        }
        // $('.validnumber').val(`${Math.random()}`.substring(3, 7));
        $('.next-btn').removeAttr('disabled');
    });

    checkInput('.input-tab');
    $('.input-tab input').on('change', function(e) {
        checkInput('.input-tab');
    });

    $('.next-btn').click(function() {
        var btnValue = $('.next-btn').text();
        if (btnValue === '下一步，填写手机号') {
            $('.next-btn').text('完成申领');
            $('.next-btn').attr('disabled', 'disabled');
            return;
        } else {
            var name = $('.name').val();
            var idCard = $('.idCard').val();
            var nation = $('.nation').val();
            var address = $('.address-detail').val();
            var phone = $('.phone').val();
            if (!/^1\d{10}$/.test(phone)) {
                return weui.topTips('手机号格式错误');
            }
            if (!checkIdCard(idCard)) return;
            if (!checkName(name)) return;

            if (name && idCard && nation && address && phone) {
                // window.location.href = 'list.html';
                $.ajax({
                    url: '/health/card',
                    data: {
                        name: name,
                        idCard: idCard,
                        nation: nation,
                        address: address,
                        phone: phone,
                    },
                    headers: {"X-CSRFToken": getCookie("csrftoken")},
                    dataType: 'json',
                    type: 'post',
                    success: function(res) {
                        console.log(res.retcode)
                        if (res.retcode == 0) {
                            console.log("创建成功")
                            var url = '/health/personal/' +res.id;
                            console.log(url)
                            window.location.href = url
                        } else {
                            weui.topTips(res.msg);
                        }
                    },
                    error: function (XmlHttpRequest,textStatus, errorThrown) {
                        alert("请求失败，请重试！");
                    }
                });
            }
        }
    });
})();

function checkInput(fa) {
    var name = $(fa + ' .name').val();
    var idCard = $(fa + ' .idCard').val();
    var nation = $(fa + ' .nation').val();
    var address = $(fa + ' .address-detail').val();
    var phone = $(fa + ' .phone').val();
    var ssmCode = $(fa + ' .validnumber').val();
    var btnValue = $('.next-btn').text();
    $('.next-btn').removeAttr('disabled');
    console.log('fa', name, idCard, nation, address, phone);
    if (name && idCard && nation && address) {
        if (btnValue === '下一步，填写手机号' || (phone)) {
            $(fa + ' .next-btn').removeAttr('disabled');
        } else {
            $(fa + ' .next-btn').attr('disabled', 'disabled');
        }
        return { status: true, data: { name, idCard, nation } };
    }
    return { status: false, data: { name, idCard, nation } };
}

function checkIdCard(idCard) {
    if (idCard.length < 18) {
        weui.topTips('身份证号码不足18位');
        return false;
    }

    return true;
}

function checkName(name) {
    if (name.length < 1) {
        weui.topTips('请输入姓名');
        return false;
    }

    return true;
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    console.log(r);
    return r ? r[1] : undefined;
}

function initPickder() {
    var nationItems = [
        {
            value: '01',
            label: '汉族'
        },
        {
            value: '02',
            label: '蒙古族'
        },
        {
            value: '03',
            label: '回族'
        },
        {
            value: '04',
            label: '藏族'
        },
        {
            value: '05',
            label: '维吾尔族'
        },
        {
            value: '06',
            label: '苗族'
        },
        {
            value: '07',
            label: '彝族'
        },
        {
            value: '08',
            label: '壮族'
        },
        {
            value: '09',
            label: '布依族'
        },
        {
            value: '10',
            label: '朝鲜族'
        },
        {
            value: '11',
            label: '满族'
        },
        {
            value: '12',
            label: '侗族'
        },
        {
            value: '13',
            label: '瑶族'
        },
        {
            value: '14',
            label: '白族'
        },
        {
            value: '15',
            label: '土家族'
        },
        {
            value: '16',
            label: '哈尼族'
        },
        {
            value: '17',
            label: '哈萨克族'
        },
        {
            value: '18',
            label: '傣族'
        },
        {
            value: '19',
            label: '黎族'
        },
        {
            value: '20',
            label: '傈僳族'
        },
        {
            value: '21',
            label: '佤族'
        },
        {
            value: '22',
            label: '畲族'
        },
        {
            value: '23',
            label: '高山族'
        },
        {
            value: '24',
            label: '拉祜族'
        },
        {
            value: '25',
            label: '水族'
        },
        {
            value: '26',
            label: '东乡族'
        },
        {
            value: '27',
            label: '纳西族'
        },
        {
            value: '28',
            label: '景颇族'
        },
        {
            value: '29',
            label: '柯尔克孜族'
        },
        {
            value: '30',
            label: '土族'
        },
        {
            value: '31',
            label: '达斡尔族'
        },
        {
            value: '32',
            label: '仫佬族'
        },
        {
            value: '33',
            label: '羌族'
        },
        {
            value: '34',
            label: '布朗族'
        },
        {
            value: '35',
            label: '撒拉族'
        },
        {
            value: '36',
            label: '毛难族'
        },
        {
            value: '37',
            label: '仡佬族'
        },
        {
            value: '38',
            label: '锡伯族'
        },
        {
            value: '39',
            label: '阿昌族'
        },
        {
            value: '40',
            label: '普米族'
        },
        {
            value: '41',
            label: '塔吉克族'
        },
        {
            value: '42',
            label: '怒族'
        },
        {
            value: '43',
            label: '乌孜别克族'
        },
        {
            value: '44',
            label: '俄罗斯族'
        },
        {
            value: '45',
            label: '鄂温克族'
        },
        {
            value: '46',
            label: '崩龙族'
        },
        {
            value: '47',
            label: '保安族'
        },
        {
            value: '48',
            label: '裕固族'
        },
        {
            value: '49',
            label: '京族'
        },
        {
            value: '50',
            label: '塔塔尔族'
        },
        {
            value: '51',
            label: '独龙族'
        },
        {
            value: '52',
            label: '鄂伦春族'
        },
        {
            value: '53',
            label: '赫哲族'
        },
        {
            value: '54',
            label: '门巴族'
        },
        {
            value: '55',
            label: '珞巴族'
        },
        {
            value: '56',
            label: '基诺族'
        }
    ];
    var cardTypeItems = [
        {
            value: '02',
            label: '居民户口簿'
        },
        {
            value: '03',
            label: '护照'
        },
        {
            value: '04',
            label: '军官证'
        },
        {
            value: '05',
            label: '驾驶证'
        },
        {
            value: '06',
            label: '港澳居民来往内地通行证'
        },
        {
            value: '07',
            label: '台湾居民来往内地通行证'
        },
        {
            value: '08',
            label: '出生证明'
        }
        // {
        //   value: '09',
        //   label: '医保卡'
        // },
        // {
        //   value: '10',
        //   label: '就诊卡'
        // },
        // {
        //   value: '11',
        //   label: '健康卡'
        // }
    ];
    var genderItems = [
        {
            value: '0',
            label: '女'
        },
        {
            value: '1',
            label: '男'
        }
    ];

    $('.select-address').on('click', function(e) {
        weui.picker(areaItems, {
            depth: 3,
            container: 'body',
            onConfirm: result => {
                $('#address-area').val(result.map(el => el.label).join(' '));
                checkInput('.input-tab');
            },
            id: 'area-picker'
        });
    });

    $('.select-gender').on('click', function(e) {
        weui.picker(genderItems, {
            container: 'body',
            defaultValue: ['01'],
            onConfirm: res => {
                $('#gender').val(res[0] && res[0].label);
                checkInput('.input-tab');
            },
            id: 'genderClick'
        });
    });

    $('.select-card-type').on('click', function(e) {
        weui.picker(cardTypeItems, {
            container: 'body',
            defaultValue: ['02'],
            onConfirm: res => {
                $('#card-type').val(res[0] && res[0].label);
                checkInput('.input-tab');
            },
            id: 'card-type'
        });
    });

    $('.select-nation').on('click', function(e) {
        weui.picker(nationItems, {
            container: 'body',
            defaultValue: ['01'],
            onConfirm: res => {
                $('#nation').val(res[0] && res[0].label);
                checkInput('.input-tab');
            },
            id: 'nationsClick'
        });
    });

    $('.select-birthday').on('click', function(e) {
        weui.datePicker({
            start: '1900-01-01',
            end: new Date(),
            defaultValue: [1985, 6, 15],
            onConfirm: result => {
                const defaultValue = [1900, 1, 1];
                const day = result
                    .map((p, index) => {
                        const value = p.value || defaultValue[index];
                        return value > 9 ? value : '0' + value;
                    })
                    .join('-');
                $('#birthday').val(day);
                checkInput('.input-tab');
            },
            id: 'birthdayClick'
        });
    });
}
