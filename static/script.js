
function showElement(element){
  var showElement = document.getElementById(element);
  if (showElement.style.display === 'none') {
    showElement.style.display = 'block';
  } else {
    showElement.style.display = 'none';
  }
  
}
