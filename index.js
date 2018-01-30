var block_host = ''
var address_list = []

$(document).ready(function () {
    fetch('http://140.92.143.212:8888/GetQuestion', {
            method: 'GET'
        })
        .then(function (res) {
            return res.json()
        }).then(function (res) {
            makeList(res.question_list)
        }).catch(function (err) {
            console.log(err)
        })

    $('.host').val(block_host)

    $('#newQuestionModal').on('show.bs.modal', e => {
        $('#ans_check').empty()
    })

    $('#new_btn').on('click', function (e) {
        let ser = $('#new_form').serialize()
        block_host = $('#host').val()
        addQuestion(ser)
    })

    $('#replyModal').on('show.bs.modal', e => {
        $('#ans_list').empty()
    })

    $('#gridCheck').on('click', e => {
        if ($(e.target).prop('checked')) {
            $('#contract_address_t').attr('disabled', false)
            $('#ch_btn_t').attr('disabled', false)
            $('#question').attr('disabled', true)
            $('#answer').attr('disabled', true)
            $('#deadline').attr('disabled', true)
        } else {
            $('#contract_address_t').attr('disabled', true)
            $('#ch_btn_t').attr('disabled', true)
            $('#question').attr('disabled', false)
            $('#answer').attr('disabled', false)
            $('#deadline').attr('disabled', false)
        }
    })

    $('#ch_btn_t').on('click', e => {
        let ser = $('#new_form').serialize()
        checkAnswer(ser)
    })

    $('#r_btn').on('click', e => {
        let ser = $('#r_form').serialize()
        ansQuestion(ser)
    })

    $('#ch_btn').on('click', e => {
        $('#r_form').find('#r_answer').attr('disabled', true)
        let ser = $('#r_form').serialize()
        checkList(ser)
    })
})

function makeList(data) {
    data.forEach((elm, idx) => {
        let ql = $('#q_template').clone()
        $(ql).removeAttr('hidden')
        $(ql).attr('id', 'q_' + idx)
        $(ql).find('.q_index').text(idx + 1)
        $(ql).find('.deadline').text(elm.deadline)
        $(ql).find('.q_content').text(elm.question)
        $(ql).find('.q_address').text(elm.contract_address)
        $(ql).find('.re_btn').data('ca', elm.contract_address)
        $('#q_list_group').append(ql)

        $(ql).find('.re_btn').on('click', e => {
            const ca = $(e.target).data('ca')
            showReplyModal(ca)
        })

        $('#contract_address_t').append('<option value="'+elm.contract_address+'">'+'Q'+(idx+1)+'_ '+elm.contract_address+'</option>')
    });
}

function addQuestion(ser) {
    fetch('http://140.92.143.212:8888/ContractDeploy?' + ser, {
            method: 'GET'
        })
        .then(function (res) {
            return res.json()
        }).then(function (res) {
            location.reload()
            console.log(res)
        }).catch(function (err) {
            console.log(err)
        })
}

function ansQuestion(ser) {
    fetch('http://140.92.143.212:8888/AnswerQuestion?' + ser, {
            method: 'GET'
        })
        .then(function (res) {
            return res.json()
        }).then(function (res) {
            console.log(res)
            location.reload()
        }).catch(function (err) {
            console.log(err)
        })
}

function checkList(ser) {
    fetch('http://140.92.143.212:8888/CheckContract?' + ser + '&behavior=checkList', {
            method: 'GET'
        })
        .then(function (res) {
            return res.json()
        }).then(function (res) {
            let html = '<span class="badge badge-dark">' + res.output + '</span>'
            $('#ans_list').append(html)
        }).catch(function (err) {
            console.log(err)
        })
    $('#r_form').find('#r_answer').removeAttr('disabled')
}

function checkAnswer(ser) {
    fetch('http://140.92.143.212:8888/CheckContract?' + ser + '&behavior=checkAnswer', {
            method: 'GET'
        })
        .then(function (res) {
            return res.json()
        }).then(function (res) {
            let html = '<span class="badge badge-dark">' + res.output + '</span>'
            $('#ans_check').html(html)
        }).catch(function (err) {
            console.log(err)
        })
}

function showReplyModal(ca) {
    $('#r_contract_address').val(ca)
    $('#replyModal').modal('show')
}