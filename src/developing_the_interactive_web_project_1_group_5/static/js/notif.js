function deleteConnection(nodeid1, nodeid2){
  // TODO: add pop-up for a check to delete or not?
  console.log("hello?")
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