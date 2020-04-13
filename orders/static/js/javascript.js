$(document).ready(function () {
 $( "#cartbutton" ).click(function() {
    console.log(this.display)
    $( "#cart-1" ).toggle('slow')
  });
});

// window.onload = function(){
//   var app =  new Vue({
//         el: '#app',
//         delimiter: ['[[',']]'],
//         data: {
//           seen: true
//       }
//     })
//   }
