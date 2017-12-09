/**
 * Created by qin on 2017/11/10.
 */
$(document)
    .ready(function () {
        $('.ui.menu .ui.dropdown').dropdown({
            on: 'click'
        });
        // $('.ui.menu a.nav-item')
        //     .on('click', function () {
        //         $(this)
        //             .addClass('active')
        //             .siblings()
        //             .removeClass('active')
        //         ;
        //     })
        // ;
    })
;

$(document)
    .ready(function () {
        $('.ui.search')
            .search()
        ;
    })
;

function enterSameName(event, target) {
    //alert ("The new content: " + event.target.value);
    var value = event.target.value;
    if (value === target) {
        $(".delete-house-btn").removeClass("disabled")
    } else {
        $(".delete-house-btn").addClass("disabled")
    }
}