
var previewImage = function(event) {
    if(event.target.files[0])
    {
      var output = document.getElementById('profileNewImagePreview');
      output.src = URL.createObjectURL(event.target.files[0]);
      output.style.width = "100px";
      $(".js-profileNewImagePreview").toggleClass("hidden")
      $(".js-profileImagePreview").toggleClass("hidden")
      output.onload = function() {
        URL.revokeObjectURL(output.src) 
      }
    }
    else
    {
      $(".js-profileImagePreview").toggleClass("hidden")
      $(".js-profileNewImagePreview").toggleClass("hidden")
    }
    
  };

$(document).on("click", ".js-try", function(e) {
    e.preventDefault()
    input = document.getElementById('user_image');
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        
        reader.onload = function (e) {
            $(".js-profileNewImage").attr('src', e.target.result);
        }
        
        reader.readAsDataURL(input.files[0]);
        $(".js-profileImage").addClass("hidden")
        $(".js-profileNewImage").removeClass("hidden")
    }
    else
    {
        $(".js-profileNewImage").addClass("hidden")
        $(".js-profileImage").removeClass("hidden")
    }
    $(".js-profileText").text($('#user_text').val())
    $(".js-profileUsername").text($('#user_username').val())
    
})

$(document).on("click", ".js-restart", function(e) {
    location.reload()
})