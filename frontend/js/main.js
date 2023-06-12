$.ajaxSetup({
    beforeSend: function beforeSend(xhr, settings) {
        function getCookie(name) {
            let cookieValue = null;


            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');

                for (let i = 0; i < cookies.length; i += 1) {
                    const cookie = jQuery.trim(cookies[i]);

                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (`${name}=`)) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }

            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        }
    },
});

$(document).on("click",".js-toggle-modal", function(e) {
    e.preventDefault()
    console.log("Hello I was clicked")
    $(".js-modal").toggleClass("hidden")
})

$(document).on("click",".js-submit", function(e) {
    e.preventDefault()
    const text = $(".js-new-post-text").val().trim()
    const $btn = $(this)
    if(!text.length){
        return false
    }

    $btn.prop("disabled", true).text("Posting!")
    $.ajax({
        type: 'POST',
        url: $(".js-new-post-text").data("post-url"),
        data: {
            text:text
        },
        success: (dataHtml) =>{
            
            $(".js-modal").addClass("hidden")
            $("#post-container").prepend(dataHtml);
            $btn.prop("disabled", false).text("New Post");
            $(".js-new-post-text").val("");
        },
        error: (error) => {
            console.warn(error)
            $btn.prop("disabled", false).text("Error");
        }
    });
})

.on("click",".js-follow", function (e) {
    e.preventDefault();
    action = $(this).attr("data-action")
    $.ajax({
        type: 'POST',
        url: $(this).data("url"),
        data: {
            action: action ,
            username: $(this).data("username")
        },
        success: (data) =>{
            $(".js-follow-text").text(data.wording)
            $(this).attr("data-action", data.wording)
            if (action == "Follow"){
                $(".js-followersNumber").text(Number($(".js-followersNumber").text())+1)
            }
            else{
                $(".js-followersNumber").text(Number($(".js-followersNumber").text())-1)
            }

        },
        error: (error) => {
            console.warn(error)
        }
    });
    
})


$(document).on("click",".js-toggle-login", function(e) {
    e.preventDefault()
    console.log("Hello I was clicked login")
    $(".js-signup").addClass("hidden")
    $(".js-login").toggleClass("hidden")
    console.log("Hello I was clicked login2")
})

