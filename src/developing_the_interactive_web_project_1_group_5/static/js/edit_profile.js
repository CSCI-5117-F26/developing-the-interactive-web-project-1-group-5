// From https://stackoverflow.com/questions/4459379/preview-an-image-before-it-is-uploaded
var picture = document.getElementById("picture");
picture.onchange = function(event) {
  const [file] = picture.files;
  if (file) {
    document.getElementsByClassName('pfp')[0].src = URL.createObjectURL(file);
  }
}