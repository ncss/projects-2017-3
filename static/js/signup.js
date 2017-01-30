$(document).ready(function(){
  document.getElementById("profile-upload-image").click();
});

function openDiv(evt, idOfElement) {
    // id of the element to unhide
    var i, tabcontent, tablinks;

    // hide all the tabs
    tabcontent = document.getElementsByClassName("profile_tab");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // show element by setting it to block
    document.getElementById(idOfElement).style.display = "block";
    evt.currentTarget.className += " active";
}
