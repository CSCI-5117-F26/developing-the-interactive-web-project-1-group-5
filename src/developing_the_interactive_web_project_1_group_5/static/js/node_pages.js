/* Referenced from https://www.w3schools.com/howto/howto_css_modals.asp example 1 */
var modal = document.getElementById("connectNodeModal");

var btn = document.getElementById("add-node");

var span = document.getElementById("close-modal");

if (btn){
  btn.onclick = function() {
  modal.style.display = "block";
}
}

if (span){
span.onclick = function() {
  modal.style.display = "none";
}
}

if (window){
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
}
// connect node modal, here we need to keep track of the selected node types so we can add to list later
let selected_nodes = [];
function selectConnection(button, node_id){
  if (button.classList.contains("selected-node")){
      button.classList.remove("selected-node");
      selected_nodes.splice(selected_nodes.indexOf(node_id), 1);
  }
  else{
      button.classList.add("selected-node");
      selected_nodes.push(node_id);
  }
  document.getElementById("add_selection").innerText = "Add " + selected_nodes.length;
}

function clearSelections(){
  selected_nodes = [];

  const nodes = document.querySelectorAll('.selected-node');

  nodes.forEach((node) => {
    node.classList.remove("selected-node");
  });
  document.getElementById("add_selection").innerText = "Add " + selected_nodes.length;
}

// https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
//https://stackoverflow.com/questions/42593178/how-can-i-do-metaname-csrf-token-attrcontent-in-vanilla-javascrip
function addSelections(node_id){
  let connections = [];
  selected_nodes.forEach((node_id2) => {
    connections.push([String(node_id), node_id2]);
  });
  const payload = { "new_connections": connections};

  fetch('/add-connections', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
      },
      body: JSON.stringify(payload)
  })
  .then(response => {
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
      clearSelections();
      window.location.reload();
      return response.json(); 
  })
  .catch(error => {
      console.error(error.message);
  });
}

function deleteConnection(nodeid1, nodeid2){
  // TODO: add pop-up for a check to delete or not?
  fetch('/delete-connections', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
      },
      body: JSON.stringify({"nodeid1": String(nodeid1), "nodeid2": String(nodeid2)})
  })
  .then(response => {
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
      window.location.reload();
      return response.json(); 
  })
  .catch(error => {
      console.error(error.message);
  });
}
