
function handleCartResult(resultData){
    console.log(resultData);
}

function displayAbout() {
    $(".about-info").slideToggle("slow");
    $(".arrow").toggleClass("down up");
    $(".popuptext").toggleClass("show");
}

function displayMessageModal(type, id) {
    // Get the modal
    let modal = document.getElementById("deleteModal");
    let span = document.getElementById("closeButton");
    if (type === "message"){
        modal = document.getElementById("messageModal");
        span = document.getElementById("close");
    } else if (type === "archive"){
        document.getElementById("modal-text").innerHTML = "Archiving will move this habit to the archived habits page, and will deactivate the habit. Archiving can be undone.";
        let btn = document.getElementById("confirm");
        btn.innerHTML = "Archive";
        btn.onclick = function() { archiveHabit(id) }
    }

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

