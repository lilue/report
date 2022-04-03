const form = document.getElementById('form');
const name = document.getElementById('name');
const idCard = document.getElementById('idCard');
const cardId = document.getElementById('cardId');

// Show input error message
function showError(input, message) {
    const fromControl = input.offsetParent;
    fromControl.className = 'weui-cell error';
    const small = fromControl.querySelector('small');
    small.innerText = message;
}

// Show success outline
function showSuccess(input) {
    const formControl = input.offsetParent;
    formControl.className = 'weui-cell success';
}

// Check required fields
function checkRequired(inputArr) {
    let isRequired = false;
    inputArr.forEach(function (input) {
        if (input.value.trim() === '') {
            showError(input, `${getFieldName(input)}是必填项`);
            isRequired = true;
        } else {
            showSuccess(input);
        }
    });
    return isRequired;
}

// Check input length
function checkLength(input, min, max) {
    if (input.value.length < min) {
        showError(input, `${getFieldName(input)}至少 ${min} 个字符`);
    } else if (input.value.length > max) {
        showError(input, `${getFieldName(input)}至多 ${max} 个字符`);
    }
}

// Get field_name
function getFieldName(input) {
    const formControl = input.offsetParent;
    // console.log(input.offsetParent);
    const label = formControl.querySelector('label');
    return label.innerText;
}
//
// form.addEventListener('submit', function(e) {
//     e.preventDefault();
//     if (checkRequired([name, idCard, cardId])) {
//         checkLength(name, 2, 6);
//         checkLength(idCard, 15, 18);
//     } else {
//         $('#btn_loading').html('<i class="weui-loading"></i>表单提交中');
//         // showToastMessage();
//         $('form').unbind('submit').submit();
//     }
// });
