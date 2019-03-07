//////////////Wrapper for to be executed only when page finished loading
document.addEventListener('DOMContentLoaded', () => {

    $(document).on("click","#submit",submit);


    ////////////////////////////////////////////////////////////////
    //These functions are required to obtain CSRF code and attach it to POST methods
    
            // CSRF code
            function getCookie(name) {
                var cookieValue = null;
                var i = 0;
                if (document.cookie && document.cookie !== '') {
                    var cookies = document.cookie.split(';');
                    for (i; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            var csrftoken = getCookie('csrftoken');
        
            function csrfSafeMethod(method) {
                // these HTTP methods do not require CSRF protection
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }
            $.ajaxSetup({
                crossDomain: false, // obviates need for sameOrigin test
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type)) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            }); 
    /////////////////////////////////////////////////////////////////
    });

function submit(){
    //get variables to pass
    name = $('#name').text();
    ticker = $('#ticker').text();
    price = $('#price').text();
    message = $('textarea#investment-case-input').val();
    target = $('#target-price-input').val();
    
    //make ajax post request
     $.ajax({
        type: "POST",
        url: "/record_trade",
        dataType: "json",
        data: {"name": name, "ticker": ticker, "price":price, "message":message, "target":target},

    });
    window.location.pathname = 'dashboard';
} 


