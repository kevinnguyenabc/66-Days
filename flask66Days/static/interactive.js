
function handleCartResult(resultData){
    console.log(resultData);
}

function displayAbout() {
    $(".about-info").slideToggle("slow");
    $(".arrow").toggleClass("down up");
    $(".popuptext").toggleClass("show");
}

function displayMessageModal(type) {
    // Get the modal
    let modal = document.getElementById("messageModal");
    var span = document.getElementById("close");
    if (type === "delete"){
        modal = document.getElementById("deleteModal");
        span = document.getElementById("closeButton");
    } 

    // Get the <span> element that closes the modal


    // When the user clicks on the button, open the modal
    modal.style.display = "block";

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";   
        }
    }
}

