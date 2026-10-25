// From https://stackoverflow.com/questions/4459379/preview-an-image-before-it-is-uploaded
var picture = document.getElementById("picture");
if (picture){
  picture.onchange = function(event) {
    const [file] = picture.files;
    if (file) {
      // Check smaller than 4 mb
      if (file.size > 4 * 1024 * 1024) {
          alert("Image size is too large!");
          picture.value = "";
          return;
      }
      img = document.getElementById('nodeImg') || document.getElementsByClassName('pfp')[0];
      img.src = URL.createObjectURL(file);
    }
  }
  
}


// Char counter
const textToCount = document.getElementById("node_description") || document.getElementById("bio");
const charCount = document.getElementById("char_count");

if (textToCount){
    function updateCharCount() {
        charCount.textContent = `${textToCount.value.length} / 240`;
    }

    textToCount.addEventListener("input", updateCharCount);

    updateCharCount();
}