/*
 *  jquery-easy-loading - v1.3.0
 *  Easily add and manipulate loading states of any element on the page
 *  http://github.com/CarlosBonetti/jquery-loading
 *
 *  Made by Carlos Bonetti <carlosb_bc@hotmail.com>
 *  Under MIT License
 */
! function (a) {
    "use strict";
    if ("undefined" == typeof window) throw new Error("Could not find DOM window object.");
    "function" == typeof define && define.amd ? define(["jquery", window], a) : "object" == typeof exports ? a(require("jquery"), window) : a(jQuery, window)
}(function (a, b, c) {
    var d = function (b, c) {
        this.element = b, this.settings = a.extend({}, d.defaults, c), this.settings.fullPage = this.element.is("body"), this.init(), this.settings.start && this.start()
    };
    d.defaults = {
        overlay: c,
        zIndex: c,
        message: "Loading...",
        theme: "light",
        shownClass: "loading-shown",
        hiddenClass: "loading-hidden",
        stoppable: !1,
        start: !0,
        onStart: function (a) {
            a.overlay.fadeIn(150)
        },
        onStop: function (a) {
            a.overlay.fadeOut(150)
        },
        onClick: function () {}
    }, d.setDefaults = function (b) {
        d.defaults = a.extend({}, d.defaults, b)
    }, a.extend(d.prototype, {
        init: function () {
            this.isActive = !1, this.overlay = this.settings.overlay || this.createOverlay(), this.resize(), this.attachMethodsToExternalEvents(), this.attachOptionsHandlers()
        },
        createOverlay: function () {
            var b = a('<div class="loading-overlay loading-theme-' + this.settings.theme + '"><div class="loading-overlay-content">' + this.settings.message + "</div></div>").addClass(this.settings.hiddenClass).hide().appendTo("body"),
                c = this.element.attr("id");
            return c && b.attr("id", c + "_loading-overlay"), b
        },
        attachMethodsToExternalEvents: function () {
            var c = this;
            c.element.on("loading.start", function () {
                c.overlay.removeClass(c.settings.hiddenClass).addClass(c.settings.shownClass)
            }), c.element.on("loading.stop", function () {
                c.overlay.removeClass(c.settings.shownClass).addClass(c.settings.hiddenClass)
            }), c.settings.stoppable && c.overlay.on("click", function () {
                c.stop()
            }), c.overlay.on("click", function () {
                c.element.trigger("loading.click", c)
            }), a(b).on("resize", function () {
                c.resize()
            }), a(function () {
                c.resize()
            })
        },
        attachOptionsHandlers: function () {
            var a = this;
            a.element.on("loading.start", function (b, c) {
                a.settings.onStart(c)
            }), a.element.on("loading.stop", function (b, c) {
                a.settings.onStop(c)
            }), a.element.on("loading.click", function (b, c) {
                a.settings.onClick(c)
            })
        },
        calcZIndex: function () {
            return this.settings.zIndex !== c ? this.settings.zIndex : (parseInt(this.element.css("z-index")) || 0) + 1 + this.settings.fullPage
        },
        resize: function () {
            var a = this,
                b = a.element,
                c = b.outerWidth(),
                d = b.outerHeight();
            this.settings.fullPage && (d = "100%", c = "100%"), this.overlay.css({
                position: a.settings.fullPage ? "fixed" : "absolute",
                zIndex: a.calcZIndex(),
                top: b.offset().top,
                left: b.offset().left,
                width: c,
                height: d
            })
        },
        start: function () {
            this.isActive = !0, this.resize(), this.element.trigger("loading.start", this)
        },
        stop: function () {
            this.isActive = !1, this.element.trigger("loading.stop", this)
        },
        active: function () {
            return this.isActive
        },
        toggle: function () {
            this.active() ? this.stop() : this.start()
        },
        destroy: function () {
            this.overlay.remove()
        }
    });
    var e = "jquery-loading";
    a.fn.loading = function (b) {
        return this.each(function () {
            var f = a.data(this, e);
            f ? b === c ? f.start() : "string" == typeof b ? f[b].apply(f) : (f.destroy(), a.data(this, e, new d(a(this), b))) : b !== c && "object" != typeof b && "start" !== b && "toggle" !== b || a.data(this, e, new d(a(this), b))
        })
    }, a.fn.Loading = function (b) {
        var f = a(this).data(e);
        return f && b === c || a(this).data(e, f = new d(a(this), b)), f
    }, a.expr[":"].loading = function (b) {
        var c = a.data(b, e);
        return !!c && c.active()
    }, a.Loading = d
});




Array.prototype.remove = function () {
    var what, a = arguments,
        L = a.length,
        ax;
    while (L && this.length) {
        what = a[--L];
        while ((ax = this.indexOf(what)) !== -1) {
            this.splice(ax, 1);
        }
    }
    return this;
};


var block_host = ''
var address_list = [],
    colorSet = [
        '#ffc107',
        '#6c757d',
        '#007bff',
        '#dc3545',
        '#28a745',
        '#17a2b8',
        '#343a40'
    ]
var userAry = []
userAry.length = 0
var userPair = new Object

var voteRightAry = []
voteRightAry.length = 0

var v_list = []
v_list.length = 0

var flag = 1 //是否登入之標的

// var ip = 'http://140.92.143.82:8080'
var ip = '..'

$(document).ready(function () {
    getVoteAPI()

    fetch(ip+'/GetVoter', {
        method: 'GET'
    }).then(function (res) {
        return res.json()
    }).then(function (res) {
        userAry = res.voters_list
        buildPari(userAry)
        genTable(userAry)
    }).catch(function (err) {
        console.log(err)
    })

    $('#signOutBtn').on('click', e => {
        sessionStorage.clear();
        flag = 1
        location.reload(true);
    })

    $('#deadline').datepicker({
        dateFormat: 'yymmdd'
    });

    // $('.host').val(block_host)

    // $('#newQuestionModal').on('show.bs.modal', e => {
    //     $('#ans_check').empty()
    // })

    $('#votes_btn').on('click', function (e) {
        $('body').loading()
        let ca = $('#votes_btn').data('ca')
        let reqAry = $('.e_vote_count').map((idx, elm) => {
            let voter = $(elm).attr('id').split('_')[1]
            let count = $(elm).val()
            if (count > 0) {
                // console.log('http://140.92.143.82:8888/Vote?host=' + sessionStorage.getItem('userHost') + '&account=' + sessionStorage.getItem('user') + '&passwd=' + sessionStorage.getItem('psw') + '&contract_address=' + ca + '&to_Voter=' + voter + '&cnt=' + count)
                return new Promise((rev, rej) => {
                    fetch(ip+'/Vote?host=' +
                        sessionStorage.getItem('userHost') + '&account=' +
                        sessionStorage.getItem('user') + '&passwd=' +
                        // sessionStorage.getItem('psw') + '&contract_address=' +
                        '123' + '&contract_address=' +
                        ca + '&to_Voter=' + voter + '&cnt=' + count, {
                            method: 'GET'
                        }).then(function (res) {
                        return res.json()
                    }).then(function (res) {
                        rev(res)
                    }).catch(function (err) {
                        rej(err)
                    })
                })
            }
        })

        Promise.all(reqAry).then(res => {
            // makeList(v_list)
            // dosignin({
            //     host: sessionStorage.getItem('userHost'),
            //     user: sessionStorage.getItem('user'),
            //     psw: sessionStorage.getItem('psw')
            // })
            $('#voteModal').modal('hide')
            setTimeout(function () {
                location.reload(true);
            }, 3000)
        }).catch(fail => {
            $('body').loading('toggle')
            console.log(fail)
        })
    })

    $('#newVoteBtn').on('click', e => {
        $('#voteModal').modal('show')
        voteRightAry.length = 0
        genTable(userAry)
        $('#addOptionsForm').show()
        $('#add_opts').show()
        $('#splitTickets').show()
        $('.newOptions').remove();
        $('#topic').val('').removeAttr('disabled')
        $('#deadline').val('').removeAttr('disabled')
        $('.hinttext').hide()
        $('#newVote_btn').show()
        $('#votes_btn').hide()
        $('.vote_options').remove();
    })

    $('#add_opts').on('click', e => {
        let op = $('.firstTemp').clone()
        $(op).removeClass('firstTemp')
        $(op).addClass('newOptions')
        $(op).find('input').val('')
        $('#addOptionsForm .form-row').append(op)
    })

    // $('#replyModal').on('show.bs.modal', e => {
    //     $('#ans_list').empty()
    // })

    // $('#gridCheck').on('click', e => {
    //     if ($(e.target).prop('checked')) {
    //         $('#contract_address_t').attr('disabled', false)
    //         $('#ch_btn_t').attr('disabled', false)
    //         $('#question').attr('disabled', true)
    //         $('#answer').attr('disabled', true)
    //         $('#deadline').attr('disabled', true)
    //     } else {
    //         $('#contract_address_t').attr('disabled', true)
    //         $('#ch_btn_t').attr('disabled', true)
    //         $('#question').attr('disabled', false)
    //         $('#answer').attr('disabled', false)
    //         $('#deadline').attr('disabled', false)
    //     }
    // })

    // $('#ch_btn_t').on('click', e => {
    //     let ser = $('#new_form').serialize()
    //     checkAnswer(ser)
    // })

    $('#r_btn').on('click', e => {
        // let host = $('#signin_host').val()
        let user = $('#signin_user').val()
        let psw = $('#signin_psw').val()

        fetch(ip+'/GetUserInfo?Uname=' + user + '&Upasswd=' + psw, {
            method: 'GET'
        }).then(function (res) {
            return res.json()
        }).then(function (res) {
            ary = JSON.parse(res.output)
            if (ary[0] !== '' && ary[1] !== '') {
                flag = 0
                dosignin({
                    host: ary[1],
                    user: ary[0],
                    uname: user,
                    psw
                })
            }else{
                alert('帳號密碼錯誤，請重新輸入')
            }

        }).catch(function (err) {
            console.log(err)
            alert('帳號密碼錯誤，請重新輸入')
        })
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

    // $('#ch_btn').on('click', e => {
    //     $('#r_form').find('#r_answer').attr('disabled', true)
    //     let ser = $('#r_form').serialize()
    //     checkList(ser)
    // })

    $('#newVote_btn').unbind().bind('click', e => {
        let topic = $('#topic').val()
        let deadline = $('#deadline').val()
        // let Pnum = $('#splitTKCount').val()

        let prop = []
        prop.length = 0
        $('.vote_opts').map((idx, elm) => {
            if ($(elm).val() && $(elm).val() !== '') {
                prop.push($(elm).val())
            }
        })
        $('#voteModal').modal('hide')
        $('body').loading()
        // console.log(encodeURI('http://140.92.143.82:8888/VoteContractDeploy?host=' + sessionStorage.getItem('userHost') + '&account=' + sessionStorage.getItem('user') + '&passwd=' + sessionStorage.getItem('psw') + '&topic=' + topic + '&Pnum=' + prop.length + '&prop=' + prop.join(',,,') + '&deadline=' + deadline))
        fetch(encodeURI(ip+'/VoteContractDeploy?host=' +
            sessionStorage.getItem('userHost') + '&account=' + sessionStorage.getItem('user') +
            '&passwd=' + '123' + '&topic=' + topic + '&Pnum=' + prop.length +
            '&prop=' + prop.join(',,,') + '&deadline=' + deadline), {
            method: 'GET'
        }).then(function (res) {
            return res.json()
        }).then(function (res) {
            console.log(res)
            setVoteRight(res['contract address'])
        }).catch(function (err) {
            console.log(err)
        })
    })

    $('#seletFilter').on('change', e => {
        if ($(e.target).val() == '0') {
            getVoteAPI()
            $('.noData').remove()
        } else {
            dosignin({
                host: sessionStorage.getItem('userHost'),
                user: sessionStorage.getItem('user'),
                psw: sessionStorage.getItem('psw'),
                uname: sessionStorage.getItem('uname')
            })
        }
    })
})

function getVoteAPI() {
    fetch(ip+'/GetAppInfo?app=Vote', {
            method: 'GET'
        })
        .then(function (res) {
            return res.json()
        }).then(function (res) {
            v_list = JSON.parse(res.output)
            makeList(v_list)
        }).catch(function (err) {
            console.log(err)
        })
}

function buildPari(ary) {
    for (var i = 0; i < ary.length; i++) {
        uName = ary[i].Uname
        userPair[uName] = ary[i]
    }
}

function setVoteRight(add) {
    console.log(add)
    if ($('#checkall').is(':checked')) {
        fetch(encodeURI(ip+'/VoteRight?host=' + sessionStorage.getItem('userHost') + '&account=' + sessionStorage.getItem('user') + '&passwd=' + '123' + '&contract_address=' + add + '&voter=AllUser'), {
            method: 'GET'
        }).then(function (res) {
            return res.json()
        }).then(function (res) {
            console.log(res)
            $('#voteModal').modal('hide')
            location.reload(true);
        }).catch(function (err) {
            console.log(err)
        })
    } else {
        var pary = voteRightAry.map(elm => {
            return new Promise((rev, rej) => {
                fetch(encodeURI(ip+'/VoteRight?host=' + sessionStorage.getItem('userHost') + '&account=' + sessionStorage.getItem('user') + '&passwd=' + '123' + '&contract_address=' + add + '&voter=' + elm), {
                    method: 'GET'
                }).then(function (res) {
                    return res.json()
                }).then(function (res) {
                    rev(res)
                }).catch(function (err) {
                    rej(err)
                })
            })
        })

        Promise.all(pary).then(res => {
            console.log(res)
            $('#voteModal').modal('hide')
            location.reload(true);
        }).catch(fail => {
            console.log(fail)
        })
    }
}

function genTable(data) {
    $('#st_table').DataTable({
        "oLanguage": {
            "sEmptyTable": "查無資料",
            "sSearch": "搜尋",
            "sZeroRecords": "查無相符資料",
            "oPaginate": {
                "sPrevious": "上一頁",
                "sNext": "下一頁"
            }
        },
        "bDestroy": true, //清掉原本Table的內容 
        'data': userAry,
        "columnDefs": [{
            "width": "10%",
            "targets": 0,
            'render': function (data, type, row, meta) {
                return '<input class="usercheck" type="checkbox" value="' + data + '" id="' + data + '">'
            },
            orderable: false,
        }],
        "columns": [{
                "data": "Uhash"
            },
            {
                "data": "Uname"
            },
            {
                "data": "Uhash"
            }
        ],
        "rowCallback": function (row, data, index) {
            $('.usercheck', row).on('change', function (e) {
                if ($(e.target).is(':checked')) {
                    voteRightAry.push(data.Uhash)
                } else {
                    voteRightAry.remove(data.Uhash)
                }
            })
        },
        "drawCallback": function (settings) {
            if ($('#checkall').is(':checked')) {
                $('.usercheck').each((idx, elm) => {
                    $(elm).attr('checked', true)
                })
            } else {
                $('.usercheck').each((idx, elm) => {
                    $(elm).attr('checked', false)
                })
            }
        }
    })

    $('#st_table_length').hide()
    $('#st_table_info').hide()
    $('#checkall').unbind().bind('change', e => {
        if ($(e.target).is(':checked')) {
            voteRightAry = userAry.map(elm => elm.Uhash)
            $('.usercheck').each((idx, elm) => {
                $(elm).attr('checked', true)
            })
        } else {
            voteRightAry.length = 0
            $('.usercheck').each((idx, elm) => {
                $(elm).attr('checked', false)
            })
        }
    })
}

function makeList(data, avalible) {
    $('.q_list').not($('#q_template')).remove()
    data.forEach((elm, idx) => {
        if (!elm) {
            return false
        }
        let ql = $('#q_template').clone()
        $(ql).addClass('listAddClass')
        $(ql).removeAttr('hidden')
        $(ql).attr('id', 'q_' + idx)
        $(ql).find('.q_index').text(idx + 1)
        // $(ql).find('.organizer').text(elm.account)
        $(ql).find('.deadlineDate').removeClass('text-danger')
        $(ql).find('.deadlineDate').text(elm.deadline)
        $(ql).find('.q_title').text(elm.topic)
        $(ql).find('.fakeForm_temp').addClass('fakeForm')

        $(ql).find('.account').val(elm.account)
        $(ql).find('.contract_address').val(elm.contract_address)
        $(ql).find('.props').val(elm.prop)
        // $(ql).find('.q_address').text(elm.contract_address)
        $(ql).find('.re_btn').data('data', elm)

        $(ql).find('.collapse').attr('id', 'collapse_' + elm.contract_address)
        $(ql).find('.collapseBtn').attr('data-target', '#collapse_' + elm.contract_address)
        $(ql).find('.collapseBtn').attr('aria-controls', '#collapse_' + elm.contract_address)

        $('#q_list_group').append(ql)


        if (avalible) {
            let d1 = new Date(elm.deadline)
            let d2 = new Date()
            if (d2 > d1) {
                $(ql).find('.deadlineDate').addClass('text-danger')
            } else {
                $(ql).find('.re_btn').removeAttr('hidden')

                $(ql).find('.re_btn').on('click', e => {
                    const data = $(e.target).data('data')
                    console.log(data)
                    let cas = $(ql).find('.fakeForm').find('.contract_address').val() //contract address
                    console.log(data.cas)
                    showReplyModal({
                        cas,
                        ...data
                    })
                })
                $('#contract_address_t').append('<option value="' + elm.contract_address + '">' + 'Q' + (idx + 1) + '_ ' + elm.contract_address + '</option>')

                $(ql).find('.collapseBtn').removeAttr('hidden')
                $(ql).find('.collapseBtn').on('click', e => {
                    tickNum(elm, $(ql))
                })
            }
        }
    });

    if ($('.listAddClass').length == 0) {
        $('.noData').remove()
        $('#q_list_group').append('<h3 class="noData text-center text-muted">No Votes are Avaliable</h3>')
    }

    if (flag == 1 && sessionStorage.length !== 0) {
        flag = 0
        dosignin({
            host: sessionStorage.getItem('userHost'),
            user: sessionStorage.getItem('user'),
            psw: sessionStorage.getItem('psw'),
            uname: sessionStorage.getItem('uname')
        })
    }
}

function makeChart(ctx, data) {
    let myBarChart = new Chart(ctx, {
        type: 'horizontalBar',
        color: [
            '#ffc107',
            '#dc3545',
            '#6c757d',
            '#28a745',
            '#007bff',
        ],
        data: data,
        options: {
            legend: {
                display: false
            },
            scales: {
                xAxes: [{
                    ticks: {
                        beginAtZero: true,
                        stepSize: 1
                    }
                }]
            }
        }
    });
}

function dosignin(data) {
    let pa = $('.fakeForm').map((idx, elm) => {
        let ca = $(elm).find('.contract_address').val()
        // console.log('http://140.92.143.82:8888/CheckVoteContract?host='+data.host+'&contract_address='+ca+'&behavior=GetRemainVoteWeight&arg='+data.user)
        return new Promise((rev, rej) => {
            fetch(ip+'/CheckVoteContract?host=' + data.host + '&contract_address=' + ca + '&behavior=GetRemainVoteWeight&arg=' + data.user, {
                method: 'GET'
            }).then(function (res) {
                return res.json()
            }).then(function (res) {
                rev({
                    output: res.output,
                    idx,
                    ca
                })
            }).catch(function (err) {
                rej(err)
            })
        })
    })

    Promise.all(pa).then(res => {
        filterChart(res);
        $('#avaliableOPT').remove()
        $('#seletFilter').append($('<option id="avaliableOPT"></option>').text('可投票列表').val('1'))
        $('#seletFilter').val('1')
        sessionStorage.setItem('user', data.user)
        sessionStorage.setItem('uname', data.uname)
        sessionStorage.setItem('userHost', data.host)
        sessionStorage.setItem('psw', data.psw)
        $('#signOutBtn').show();
        $('#signInBtn').hide();
        $('#newVoteBtn').show();
        $('#editAccount').show();
        setUserProfile();
        $('#signinModal').modal('hide')
    }).catch(fail => {
        console.log(fail)
    })
}

function tickNum(elm, $ql) {
    fetch(ip+'/GetTicketNumber?host=' + sessionStorage.getItem('userHost') + '&contract_address=' + elm.contract_address + '&prop=' + elm.prop, {
            method: 'GET'
        })
        .then(function (res) {
            return res.json()
        }).then(function (res) {
            console.log(res)

            let ctx = $($ql).find('.chart_div')
            let elmJson = JSON.parse(res.output)
            let lb = []
            lb.length = 0
            let dt = []
            dt.length = 0

            for (let i in elmJson) {
                lb.push(i)
                dt.push(elmJson[i])
            }

            let cc = (() => {
                let dtl = dt.length
                let csl = colorSet.length
                let rt = []
                rt.length = 0

                if (dtl > csl) {
                    let count = dtl / csl
                    for (var i = 0; i < count; i++) {
                        rt = rt.concat(colorSet)
                    }
                    return rt
                } else {
                    return colorSet
                }
            })();

            let data = {
                labels: lb,
                datasets: [{
                    label: 'Vote ' + elm.topic,
                    data: dt,
                    backgroundColor: cc,
                }]
            }
            makeChart(ctx, data)
        }).catch(function (err) {
            console.log(err)
        })
}

function filterChart(data) {
    let cloneAry = v_list.slice(0)
    for (let i = 0; i < data.length; i++) {
        const elm = data[i];
        if (elm.output == '0') {
            cloneAry.splice(elm.idx, 1, null)
        } else {
            sessionStorage.setItem('q_' + elm.ca + '_count', elm.output)
        }
    }
    makeList(cloneAry, true)
}

function setUserProfile() {
    // $('#g_userid').text('帳戶: ' + sessionStorage.getItem('user'))
}

function showReplyModal(data) {
    $('.vote_options').remove();
    $('.newOptions').remove();
    $('.hinttext').show()
    $('#addOptionsForm').hide()
    $('#add_opts').hide()
    $('#splitTickets').hide()

    $('#newVote_btn').hide()
    $('#votes_btn').show()
    $('#topic').val(data.topic).attr('disabled', true)
    $('#deadline').val(data.deadline).attr('disabled', true)
    $('#votes_btn').data('ca', data.contract_address)
    let opts = data.prop.split(',,,')
    $('#hint_num').text(sessionStorage.getItem('q_' + data.contract_address + '_count'))
    for (var i = 0; i < opts.length; i++) {
        let os = $('#tempOptionsForm').clone()
        $(os).removeAttr('hidden')
        $(os).addClass('vote_options')
        $(os).attr('id', data.contract_address + '_' + i)
        $(os).find('.vote_check').attr('id', i)
        $(os).find('.vote_check_lable').attr('for', i)
        $(os).find('.vote_check_lable').text(opts[i])
        $(os).find('.vote_count').attr('id', 'voter_' + i)
        $(os).find('.vote_count').addClass('e_vote_count')
        $('#tempOptionsForm').after(os)

        $(os).find('.vote_check').on('change', (e) => {
            let trf = $(e.target).is(':checked')
            if (trf) {
                $(os).find('.vote_count').val(1).removeAttr('disabled').trigger('input')
            } else {
                $(os).find('.vote_count').val(0).attr('disabled', true)
            }
        })
    }
    $('#voteModal').modal('show')

    limit_count = sessionStorage.getItem('q_' + data.contract_address + '_count')

    $('.vote_count').unbind().bind('input', (e) => {
        let totalcount = 0
        $('.vote_count').each((idx, elm) => {
            if ($(elm).val() > 0) {
                totalcount += parseInt($(elm).val())
                if (totalcount > limit_count) {
                    $(elm).val(0)
                }
            }
        })
    })
}