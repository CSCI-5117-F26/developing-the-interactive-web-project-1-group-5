/* Referenced from https://www.w3schools.com/howto/howto_css_modals.asp example 1 */
var modal = document.getElementById("connectNodeModal");

var btn = document.getElementById("addNode");

var span = document.getElementsByClassName("close")[0];

btn.onclick = function() {
  modal.style.display = "block";
}

span.onclick = function() {
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

// connect node modal, here we need to keep track of the selected node types so we can add to list later
function selectConnection(button){
    if (button.classList.contains("selected-node")){
        button.classList.remove("selected-node");
    }
    else{
        button.classList.add("selected-node");
    }
}