var cartArray = [];
var checkArray = [];
let span = document.getElementById("NumOfItems");

// Function to retrieve cartArray from the cookie
function getCartCookie() {
  var cookieValue = document.cookie.replace(/(?:(?:^|.*;\s*)cartArray\s*=\s*([^;]*).*$)|^.*$/, "$1");
  if (cookieValue) {
    // Parse the JSON string to get the array
    cartArray = JSON.parse(cookieValue);
    updateCartDisplay();
  }
}

// Function to update the cart display
function updateCartDisplay() {
  numOfProducts = cartArray.length;
  span.textContent = numOfProducts;
  console.log(numOfProducts);
  console.log(cartArray);
  console.log(checkArray);
}

// Function to add an item to the cart
function cartSession(product_id, product_name, product_price)  {
  checkArray.push(product_id);
  cartArray.push({product_id, product_name, product_price});
  updateCartDisplay();
  setCartCookie(); // Call setCartCookie whenever you modify the cartArray
  setCheckCookie();
}

function setCartCookie() {
  var cartArrayString = JSON.stringify(cartArray);
  document.cookie = "cartArray=" + cartArrayString + "; path=/";
  console.log("Cookie set");
}

function setCheckCookie() {
  var checkArrayString = JSON.stringify(checkArray);
  document.cookie = "checkArray=" + checkArrayString + "; path=/";
  console.log("Cookie set");
}

function clearCart(){ 
  cartArray= [];
  checkArray = [];
  updateCartDisplay();
  document.cookie = "cartArray=; expires= Thu, 01 Jan 2024 00:00:00 UTC; path=/;";
  document.cookie = "checkArray=; expires= Thu, 01 Jan 2024 00:00:00 UTC; path=/;";
  console.log("Cart cleared", cartArray)
}

function showElement(element){
  var showElement = document.getElementById(element);
  if (showElement.style.display === 'none') {
    showElement.style.display = 'block';
  } else {
    showElement.style.display = 'none';
  }
  
}


// Call getCartCookie on page load to retrieve the cartArray
window.onload = function () {
  getCartCookie();
};




// function toggleAnswerShow(parentId) {
//   var answerShowElement = document.getElementById('answerShow');
//   if (answerShowElement.style.display === 'none' || answerShowElement.style.display === '') {
//       answerShowElement.style.display = 'block';
//       // Här kan du göra något med parentId, till exempel lägga det i en input eller en variabel
//       document.querySelector('#answerShow input[name="parent_id"]').value = parentId;
//   } else {
//       answerShowElement.style.display = 'none';
//   }
// }



