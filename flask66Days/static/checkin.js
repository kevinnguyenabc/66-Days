function handleCheckIn(id){
    button = $("#"+id)
    button.html('Checked In! &#10003;');
    button.addClass("checked_in");
    button.removeClass("check_in");
    button.prop("onclick", null);
    $("#habit-"+id).css("transform", "scale(1.1)")
    setTimeout( function () { $("#habit-"+id).css("transform", "scale(1.02)") }, 300); 
    let counter = $("#streak-counter");
    console.log(counter.text())
    let days = counter.text().split(" ")[0];
    counter.text((parseInt(days)+1) + " Days");
    let progress = $("div.progress-text");
    console.log(progress);
    days = progress.text().split(" ")[0];
    progress.text((parseInt(days)+1) + " Days Completed");
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
    // Could have just called this using url_for in html, but can be used if want to send ajax 
    jQuery.ajax({
        dataType: "text",  // Setting return data type
        method: "POST",// Setting request method
        url: "/single_habit/" + id + "/delete", // Setting request url, mapped to routes.py
        success: (url) => handleDeleteHabit(url) // Setting callback function to handle data returned successfully by the SingleStarServlet
    });
}

function archiveHabit(id){
    jQuery.ajax({
        dataType: "text",  // Setting return data type
        method: "POST",// Setting request method
        url: "/single_habit/" + id + "/archive", // Setting request url, mapped to routes.py
        success: function(url){
            window.location.href = url;
        } // Setting callback function to handle data returned successfully by the SingleStarServlet
    });
}