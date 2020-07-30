
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
    let btn = $("#confirm");
    if (type === "message"){
        modal = document.getElementById("messageModal");
        span = document.getElementById("close");
    } else if (type === "archive"){
        btn.show();
        modal = document.getElementById("updateModal");
        span = document.getElementById("closeButton2");
        document.getElementById("modal-text").innerHTML = "\nArchiving will move this habit to the archived habits page, and will deactivate the habit. Archiving can be undone.";
        document.getElementById("link-username").style.display = "none";
        btn.text("Archive");
    } else if (type === "link"){
        btn.show();
        modal = document.getElementById("updateModal");
        span = document.getElementById("closeButton2");
        document.getElementById("modal-text").innerHTML = "\nWho would you like to link this habit with?";
        document.getElementById("link-username").style.display = "block";
        btn.text("Link");
        btn.attr("onclick", "linkRequest("+id+")");
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

function openMessage(messageId, messageType){
    let modal = document.getElementById("inboxMessageModal");
    let span = document.getElementById("closeButton2");
    document.getElementById("modal-text").innerHTML = "\nChoose which habit to link!";
    let btn = document.getElementById("confirm");
    btn.onclick = function() { 
        console.log(messageType.split(":")[1]);
        console.log(document.getElementById("habit-chosen").value);
        linkHabits(messageType.split(":")[1], document.getElementById("habit-chosen").value, messageId)
    }
    // btn.attr("onclick", "linkHabits("+id+")");

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