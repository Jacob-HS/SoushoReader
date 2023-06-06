

var socket = io();

socket.on("answer", function(data){
  console.log("recieved");
  console.log(data["data"]);
  displayQuestionImage();
  displayAnswers(data["data"]);
});

document.getElementById("file").addEventListener("change", function(event){
  document.getElementById("file").files[0].arrayBuffer().then(function(result){
    var final = new Uint8Array(result);
    var blob = new Blob( [ final ], { type: "image/jpeg" } );
    var urlCreator = window.URL || window.webkitURL;
    var imageUrl = urlCreator.createObjectURL( blob );
    var img = document.getElementById("showImage");
    img.src = imageUrl;
    document.getElementById("testImage").src=imageUrl;
    let image = document.getElementById("testImage");
    const cropper = new Cropper(image, {
      autoCrop: false,
      aspectRatio: 1
    });
    const test= [...final];
    console.log(test);
    socket.emit("askQuestion", {"data": test}); 
  });
  
});
document.getElementById("questionImageHolder").addEventListener('dragover', function (event) {
  event.preventDefault();
});

document.getElementById("questionImageHolder").addEventListener("drop", function(event){
  event.preventDefault();
  console.log("hi");
  if(event.dataTransfer.items.length > 1){
    alert("One file at a time, please");
    return;
  }

  if(event.dataTransfer.items[0].kind !== "file"){
    alert("Files please.");
  }
  FILE_TYPE=event.dataTransfer.items[0].type;
  if (FILE_TYPE !== "image/png" && FILE_TYPE !== "image/jpg" && FILE_TYPE !== "image/jpeg" ){
    alert(".jpg or .png image files only, please.");
  }
  console.log(event.dataTransfer.items[0]);
  event.dataTransfer.items[0].getAsFile().arrayBuffer().then(function(result){
    var final = new Uint8Array(result);
    var blob = new Blob( [ final ], { type: "image/jpeg" } );
    var urlCreator = window.URL || window.webkitURL;
    var imageUrl = urlCreator.createObjectURL( blob );
    var img = document.getElementById("showImage");
    img.src = imageUrl;
    document.getElementById("testImage").src=imageUrl;
    const test= [...final];
    console.log(test);
    socket.emit("askQuestion", {"data": test}); 
  });
});


function displayQuestionImage(){
  document.getElementById("dragAndDropLabel").style.display="none";
  document.getElementById("showImage").style.display="block";
}

function displayAnswers(answerList){
  let i =1;
  for (const answer of answerList){
    let temp=document.getElementById("pred"+i);
    temp.innerHTML=answer;
    i++;
  }
}