function handleCheckIn(id){
    button = $("#"+id)
    button.html('Checked In! &#10003;');
    button.addClass("checked_in");
    button.removeClass("check_in");
    button.prop("onclick", null);
    $("#habit-"+id).css("transform", "scale(1.1)")
    setTimeout( function () { $("#habit-"+id).css("transform", "scale(1.02)") }, 300); 
    let counter = $("#streak-counter");
    let days = counter.text().split(" ")[0];
    counter.text((parseInt(days)+1) + " Days");
}

function handleDeleteHabit(url){
    window.location.href = url;
    console.log(url)
}

function checkin(id){
    jQuery.ajax({
        dataType: "json",  // Setting return data type
        method: "GET",// Setting request method
        url: "/check_in/" + id, // Setting request url, mapped to routes.py
        success: (id) => handleCheckIn(id) // Setting callback function to handle data returned successfully by the SingleStarServlet
    });
}

$("#deleteForm").submit(function(e) {
    e.preventDefault();
});

function deleteHabit(id){
    result = window.confirm("Are you sure you want to delete?");
    if (result) {
        jQuery.ajax({
            dataType: "text",  // Setting return data type
            method: "POST",// Setting request method
            url: "/single_habit/" + id + "/delete", // Setting request url, mapped to routes.py
            success: (url) => handleDeleteHabit(url) // Setting callback function to handle data returned successfully by the SingleStarServlet
        });
    }

}



