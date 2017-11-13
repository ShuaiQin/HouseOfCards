/**
 * Created by qin on 2017/11/10.
 */
$(document)
    .ready(function () {
        $('.ui.menu .ui.dropdown').dropdown({
            on: 'click'
        });
        $('.ui.menu a.nav-item')
            .on('click', function () {
                $(this)
                    .addClass('active')
                    .siblings()
                    .removeClass('active')
                ;
            })
        ;
    })
;
