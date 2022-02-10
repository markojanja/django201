$.ajaxSetup({
  beforeSend: function beforeSend(xhr, settings) {
    function getCookie(name) {
      let cookieValue = null;

      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let i = 0; i < cookies.length; i += 1) {
          const cookie = jQuery.trim(cookies[i]);

          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === `${name}=`) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }

      return cookieValue;
    }

    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
      // Only send the token to relative URLs i.e. locally.
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    }
  },
});

$(document).on("click", ".js-toggle-modal", function (e) {
  e.preventDefault();
  $(".js-modal").toggleClass("hidden");
}).on("click", '.js-submit', function(e){
  e.preventDefault();
  console.log("form submitted")
  const post = $('.js-post').val().trim();
  const btn = $(this);
  if(!post.length){
    return false
  }

    btn.prop("disabled", true).text("Posting");

    $.ajax({
      type:'POST',
      url:$('.js-post').data("post-url"),
      data: {
        text:post
      },
      success: (dataHtml)=>{
        $(".js-modal").addClass("hidden");
        $("#post-container").prepend(dataHtml);
        btn.prop("disabled", false).text("New Post");
        $('.js-post').val('');
      },
      error:(error)=>{
        btn.prop("disabled", false).text("Error!");
        console.log(error);
      }
    })
}).on("click", ".js-follow", function(e){
  e.preventDefault();
  let action = $(this).attr("data-action");
  // const follow = $("#follow")
  console.log('Clicked');

  $.ajax({
    type:'POST',
    url:$(this).data("follow-url"),
    data: {
      action:action,
      username:$(this).data("username"),

    },
    success: (data)=>{
      $(".js-follow-text").text(data.wording)
      console.log(data);
      if(action==="follow"){
        $(this).attr("data-action", "unfollow")
        $("#followers").text(data.total_following)

      }else{
        $(this).attr("data-action", "follow")
        $("#followers").text(data.total_following)
      }
    },
    error:(error)=>{
      console.warn(error);
     
    }
  });
}).on('click', '.js-toggle-modal-update',function(e){
  e.preventDefault();
  $(".js-modal-update").toggleClass("hidden");
}).on('click', '.js-submit-update',function(){
  console.log('btn clicked');
  const post = $('.js-post-update').val().trim();
  
  const btn = $(this);
  if(!post.length){
    console.log('empty');
    return false
  }

    btn.prop("disabled", true).text("Posting");

    $.ajax({
      type:'POST',
      url:$('.js-post-update').data("post-url"),
      data: {
        text:post
      },
      success: (dataHtml)=>{
        console.log(dataHtml);
        $(".js-modal-update").addClass("hidden");
        $("#post-container").prepend(dataHtml);
        btn.prop("disabled", false).text("New Post");
        $('.js-post-update').val('');

      },
      error:(error)=>{
        btn.prop("disabled", false).text("Error!");
        console.warn(error);
      }
    })
})


