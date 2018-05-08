$(function () {
    init();
});

function init() {
    load_data();
}

function load_data() {
    let cate_url = 'http://127.0.0.1:8000/home/cates';
    let setting = {
        type: 'GET',
        success: function (result) {
            if (result.state === 200) {
                init_cate(result.data);
                init_banner(result.banners);
            }
        },
    };
    $.ajax(cate_url, setting)
}

//创建分类菜单
function init_cate(data) {
    let $cate_ul = $('.category').mouseout(function () {
        $('.sub').toggle()
    });
    //动态创建li
    for (let cate of data) {
        $('<li>').mousemove(function () {
            let $ul = $('.sub').empty().toggle();

            for (let sub of cate.subs) {
                $('<li>').append($('<a>').text(sub.name)).appendTo($ul)
            }
        }).append($('<a>').text(cate.name)).appendTo($cate_ul)
    }
}

function init_banner(banners) {
    if (banners.length > 0) {
        for (let banner of banners) {
            $('<li>').append($('<a>')
                .append($('<img>')
                    .attr('src', 'http://127.0.0.1:8000' + banner.img_addr)))
                .appendTo($('#banner>ul'))

        }
        // 开始轮播
        lunbo()
    }
}

function lunbo() {
    $('#banner').unslider({
        dots: true
    })
}