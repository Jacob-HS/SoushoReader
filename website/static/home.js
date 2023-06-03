var socket = io();

socket.on("answer", function(data){
  console.log("recieved");
  console.log(data["data"]);
  
});

document.getElementById("file").addEventListener("change", function(event){
  document.getElementById("file").files[0].arrayBuffer().then(function(result){
    var final = new Uint8Array(result);
    var blob = new Blob( [ final ], { type: "image/jpeg" } );
    var urlCreator = window.URL || window.webkitURL;
    var imageUrl = urlCreator.createObjectURL( blob );
    var img = document.getElementById("showImage");
    img.src = imageUrl;
    const test= [...final];
    console.log(test);
    socket.emit("askQuestion", {"data": test}); 
  });
  
});