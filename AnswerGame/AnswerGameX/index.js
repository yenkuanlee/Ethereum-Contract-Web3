var block_host = '';
var address_list = [];

var flag = 1; //是否登入之標的
var ip = "http://140.92.143.82:8080";
loadList();

$(document).ready(function () {
    $('#deadline').datepicker({
        dateFormat: 'yymmdd'
    });
    $('#signin_btn').on('click', e => {
        let host = $('#signin_host').val()
        let user = $('#signin_user').val()
        let psw = $('#signin_psw').val()

        fetch(ip+'/GetUserInfo?Uname=' + user + '&Upasswd=' + psw, {
            method: 'GET'
        }).then(function (res) {
            return res.json()
        }).then(function (res) {
            ary = JSON.parse(res.output)
            if (ary[0] !== '' && ary[1] !== '') {
                flag = 0;
                dosignin({
                    host: ary[1],
                    user: ary[0],
                    uname: user,
                    psw
                })
            }else{
                console.log(ary);
                alert('帳號密碼錯誤，請重新輸入')
            }

        }).catch(function (err) {
            console.log(err);
            alert('帳號密碼錯誤，請重新輸入');
        })
    })
    $('#signOutBtn').on('click', e => {
        sessionStorage.clear();
        flag = 1
        location.reload(true);
    })

    $('#editAccountModal').on('shown.bs.modal', e => {
        if (flag == 0) {
            $('#e_signin_user').val(sessionStorage.getItem('uname'))
        }
    })
    $('#ed_btn').on('click', e => {
        // let host = $('#signin_host').val()
        let user = $('#e_signin_user').val()
        let opsw = $('#e_signin_o_psw').val()
        let npsw = $('#e_signin_psw').val()

        if (opsw === sessionStorage.getItem('psw')) {
            flag = 0
            fetch(ip+'/ModifyPasswd?Uname=' + user + '&op=' + opsw + '&np=' + npsw, {
                    method: 'GET'
                })
                .then(function (res) {
                    return res.json()
                }).then(function (res) {
                    console.log(res)
                    alert('修改成功，請重新登入')
                    sessionStorage.clear();
                    flag = 1
                    location.reload(true);
                }).catch(function (err) {
                    console.log(err)
                })
        } else {
            alert('帳號密碼錯誤，請重新輸入')
        }
    })



    $('.host').val(block_host)

    $('#createQuestionModal').on('show.bs.modal', e => {
        $('#ans_right').empty()
    })

    $('#create_btn').on('click', function (e) {
        let ser  = $('#create_form').serialize();

        $(this).text("執行中...").prop("disabled", true);
        addQuestion(ser);
    })

    $('#contract_address_t').on('change', e => {
        let address = $("#contract_address_t option:selected").val();
        $("#contract_address_t option[value=0]").remove();
        checkAnswer(address);
        checkList(address);
    })

    $('#reply_btn').on('click', e => {
        let ser  = $('#reply_form').serialize();

        $(this).text("執行中...").prop("disabled", true);
        ansQuestion(ser);
    })
})

function dosignin(data) {
    sessionStorage.setItem('user', data.user)
    sessionStorage.setItem('uname', data.uname)
    sessionStorage.setItem('userHost', data.host)
    sessionStorage.setItem('psw', data.psw)
    $('#signOutBtn').show();
    $('#signInBtn').hide();
    $('#editAccount').show();
    $('#createQuestion').show();
    $('#showAnswer').show();
    $('#signinModal').modal('hide');
    $('.re_btn').show();
}

function loadList() {
    fetch(ip+'/GetQuestion', {
        method: 'GET'
    })
    .then(function (res) {
        return res.json()
    }).then(function (res) {
        makeList(res.question_list)
    }).catch(function (err) {
        console.log(err)
    })
}

function makeList(data) {
    $('#q_list_group_content').empty();
    $('#contract_address_t').html('<option value="0">請選擇</option>');
    data.forEach((elm, idx) => {
        let ql = $('#q_template').clone()
        $(ql).removeAttr('hidden')
        $(ql).attr('id', 'q_' + idx)
        $(ql).find('.q_index').text(idx + 1)
        $(ql).find('.deadline').text(elm.deadline)
        $(ql).find('.q_content').text(elm.question)
        $(ql).find('.q_address').text(elm.contract_address)
        $(ql).find('.re_btn').data('ca', elm.contract_address)

        let d1 = new Date(elm.deadline)
        let d2 = new Date()
        if (d2 > d1)
            $(ql).find('.re_btn').hide();
        $('#q_list_group_content').append(ql)

        $(ql).find('.re_btn').on('click', e => {
            const ca = $(e.target).data('ca')
            showReplyModal(ca)
        })

        $('#contract_address_t').append('<option value="'+elm.contract_address+'">'+'問題'+(idx+1)+'_ '+elm.contract_address+'</option>')
    });

    if (flag == 1 && sessionStorage.length !== 0){
        flag = 0;
        dosignin({
            host: sessionStorage.getItem('userHost'),
            user: sessionStorage.getItem('user'),
            psw: sessionStorage.getItem('psw'),
            uname: sessionStorage.getItem('uname')
        });
    }else{
        $("#signInBtn").show();
        $('#signOutBtn').hide();
        $('#editAccount').hide();
        $('#createQuestion').hide();
        $('#showAnswer').hide();
    }
}

function addQuestion(ser) {
    fetch(ip+'/ContractDeploy?host=' + sessionStorage.getItem('userHost') + '&account=' + sessionStorage.getItem('user') + '&passwd=123&' + ser, {
            method: 'GET'
        })
        .then(function (res) {
            return res.json()
        }).then(function (res) {
            alert('出題完成！');
            loadList();
            $("#createQuestionModal").modal('hide');
            $('#create_btn').text("確定").prop("disabled", false);
        }).catch(function (err) {
            console.log(err)
        })
}

function ansQuestion(ser) {
    fetch(ip+'/AnswerQuestion?host=' + sessionStorage.getItem('userHost') + '&account=' + sessionStorage.getItem('user') + '&passwd=123&' + ser, {
            method: 'GET'
        })
        .then(function (res) {
            return res.json()
        }).then(function (res) {
            alert('回答完成！');
            loadList();
            $("#replyModal").modal('hide');
            $('#reply_btn').text("送出").prop("disabled", false);
        }).catch(function (err) {
            console.log(err)
        })
}

function checkList(address) {
    fetch(ip+'/CheckContract?host=' + sessionStorage.getItem('userHost') + '&passwd=123&contract_address=' + address + '&behavior=checkList', {
            method: 'GET'
        })
        .then(function (res) {
            return res.json()
        }).then(function (res) {
            obj = JSON.parse(res.output);
            makeTable(obj);
        }).catch(function (err) {
            console.log(err)
        })
}

function checkAnswer(address) {
    $('#ans_right').html('Loading...');
    fetch(ip+'/CheckContract?host=' + sessionStorage.getItem('userHost') + '&passwd=123&contract_address=' + address + '&behavior=checkAnswer', {
            method: 'GET'
        })
        .then(function (res) {
            return res.json();
        }).then(function (res) {
            $('#ans_right').html(res.output);
        }).catch(function (err) {
            console.log(err);
        })
}

function makeTable(obj) {
    $("#ans_list tbody").empty();
    $.each(obj, function(index, element) {
        if (element == null) return;
        $("#ans_list tbody").append(
            "<tr>" +
                "<th>" + (Number(index)+1) + "</th>" +
                "<td>" + element + "</td>" +
            "</tr>");
    });
}

function showReplyModal(ca) {
    $('#r_contract_address').val(ca);
    $('#replyModal').modal('show');
}