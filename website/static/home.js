var socket = io();


document.getElementById("file").addEventListener("change", function(event){
  document.getElementById("file").files[0].arrayBuffer().then(function(result){
    var final = new Uint8Array(result);
    const test= [...final];
    console.log(test);
    socket.emit("askQuestion", {"data": test}); 
  });
  
});