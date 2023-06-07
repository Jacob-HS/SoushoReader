

var socket = io();
let cropper;
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
    document.getElementById("testImage").src=imageUrl;
    cropImage();
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
    document.getElementById("testImage").src=imageUrl;
    cropImage(); 
  });
});

document.getElementById("submitCropButton").addEventListener("click", () => {
  let result = cropper.getCroppedCanvas({fillColor: "white"});
  let img = document.getElementById("showImage");
  img.src = result.toDataURL();
  result.toBlob(tempblob => {
    tempblob.arrayBuffer().then(arr => {
      var final = new Uint8Array(arr);
      const test = [...final];
      socket.emit("askQuestion", {"data": test});
    });
  });
  cropper.destroy();
  document.getElementById("cropPopupArea").classList.add("hidden");
});

function cropImage(){
  console.log("fuck");
  document.getElementById("cropPopupArea").classList.remove("hidden");
  img=document.getElementById("testImage");
  let image = document.getElementById("testImage");
    cropper = new Cropper(image, {
        autoCrop: true,
        autoCropArea: .8,
        viewMode: 2,
        movable: false,
        minContainerWidth: 0,
        highlight: false,
        zoomable: false,
        ready(){
          cropper.setCanvasData({ height: img.clientHeight, width: img.clientWidth  });
        }
      
    });
  document.getElementById("file").value="";
}

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