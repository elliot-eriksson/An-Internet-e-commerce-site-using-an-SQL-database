// $("#collapseExample").hide();

// $("#toggle").on("click", function() {
//     $("#collapseExample").toggleClass("hidden");
// });

// $(document).ready(function() {

//     // Hide the row when the page loads
//     $("#collapseExample").hide();
  
//     // when the user clicks the checkbox, toggle the row
//     $("#toggle").click(function() {
  
//       $("#collapseExample").toggle();
  
//     })
  
//   });

// $("#toggle").on("click", function() {
//     $("#collapseExample").toggleClass("hidden");
// });

function myFunction() {
    var x = document.getElementById("collapseExample");
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }

  $("toggle").on("click", function() {
    $("#collapseExample").toggleClass('show');
  });