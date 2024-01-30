var cartArray = []
function cartSession(product_name){
  console.log(product_name)
  cartArray.push(product_name)
  console.log(cartArray)
}

function setCartCookie() {
  // Convert the cartArray to a JSON string
  var cartArrayString = JSON.stringify(cartArray);

  // Set the cookie with the cartArrayString
  document.cookie = "cartArray=" + cartArrayString + "; path=/";
  console.log("Cookie set");
 
}
