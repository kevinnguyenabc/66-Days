


// function hello() {
//     $.getJSON('/background_process_test',
//     function(data) {
//         console.log("back in js")
//     });
// }

// hello();
function test(id){
    console.log(id);
    jQuery.ajax({
        dataType: "json",  // Setting return data type
        method: "GET",// Setting request method
        url: "/check_in/" + id, // Setting request url, mapped to routes.py
        success: (resultData) => handleCartResult(resultData) // Setting callback function to handle data returned successfully by the SingleStarServlet
    });
}

function handleCartResult(resultData){
    console.log(resultData);
}

jQuery.ajax({
    dataType: "text",  // Setting return data type
    method: "GET",// Setting request method
    url: "/background_process_test/4", // Setting request url, mapped to routes.py
    success: (resultData) => handleCartResult(resultData) // Setting callback function to handle data returned successfully by the SingleStarServlet
})