var $search = $('#search');
$search.on('keyup', function () {
    console.log("Upped");
    var items = document.getElementsByClassName("block");
    var filter = document.getElementById("search").value.toUpperCase();
    for (i = 0; i < items.length; i++) {
        title = items[i].getElementsByTagName("a")[0];
        txtValue = title.textContent || title.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
            items[i].style.display = "";
            } else {
            items[i].style.display = "none";
            }
    }
});
$(document).on('click', 'button.add', function(event) {
    var text = $(event.target);
    var next = "";
    $.ajax({
                type: 'GET',
                url: '/add-to-cart',
        
                data: {
                    slug: text.next().val(),
                    quantity: text.prev().children("input").val(),
                    next: window.location.pathname
                },
        
                success: function (response) {
                    if(response.next){
                        window.location = response.next;
                    }
                    if(response.Status){
                        text.removeClass("btn-primary");
                        text.addClass("btn-danger");
                        text.html("Update cart");
                    }
                    else{
                        text.removeClass("btn-danger");
                        text.addClass("btn-primary");
                        text.html("Add to cart");
                    }
                    if(response.count){
                        document.getElementById("cart_count").innerHTML = response.count;
                    }
                    else{
                        document.getElementById("cart_count").innerHTML = "0";
                    }
                },
                error: function() {
                    console.log("failed");
                }
            });
});