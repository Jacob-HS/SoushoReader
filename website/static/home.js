

var socket = io();
let cropper;
let sampleImageData;
let preloadedImages = [];
let cropCount=0;
let totalQuestions;
let currQuestion;
let resizedImages = {};
let originalImages = {};
socket.on("answer", function(data){
  console.log("recieved");
  console.log(data);
  sampleImageData=data;
  totalQuestions=(Object.keys(data)).length;
  currQuestion=1;
  preloadImages(sampleImageData);
  displayAnswers(Object.keys(data["1"]));
  switchActiveAnswer(1,1);
});

document.getElementById("addCropButton").addEventListener("click", ()=>{
  document.getElementById("submitCropButton").classList.remove("inactiveDone");
  cropCount++;
  let img = document.getElementById("finishedCrop"+(cropCount));
  document.getElementById("cropDeleteButton"+cropCount).classList.remove("hidden");
  let sameSizeResult = cropper.getCroppedCanvas({fillColor: "white"});
  let resizedResult = cropper.getCroppedCanvas({fillColor: "white", width: 100, height: 100});
  let imgURL=sameSizeResult.toDataURL('image/jpeg');
  img.src = imgURL;
  originalImages[String(cropCount)]=imgURL;
  resizedResult.toBlob(tempblob => {
    tempblob.arrayBuffer().then(arr => {
      var final = new Uint8Array(arr);
      const imagearray = [...final];
      resizedImages[String(cropCount)]=imagearray;
    });
  cropper.clear();
  });
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

document.getElementById("dummyButton").addEventListener("click", () => {
  document.getElementById("file").click();
});

document.getElementById("submitCropButton").addEventListener("click", () => {
  cropCount=0;
  let img = document.getElementById("showImage");
  img.src = originalImages["1"];
  resetCropper();
  console.log(resizedImages);
  socket.emit("askQuestion", resizedImages);
  document.getElementById("cropPopupArea").classList.add("hidden");
  displayQuestionImage();
  let prediction1 = document.getElementById("pred1").innerHTML;
  if (prediction1===""){
    displayMatchHeader();
    removePredictionPlaceholder();
  }else{
    prepareForSubsequentQuestion();
  }
  
});

document.getElementById("pred1").addEventListener("click",()=>switchActiveAnswer(currQuestion, 1));
document.getElementById("pred2").addEventListener("click",()=>switchActiveAnswer(currQuestion, 2));
document.getElementById("pred3").addEventListener("click",()=>switchActiveAnswer(currQuestion, 3));
document.getElementById("pred4").addEventListener("click",()=>switchActiveAnswer(currQuestion, 4));
document.getElementById("pred5").addEventListener("click",()=>switchActiveAnswer(currQuestion, 5));

document.getElementById("questionImageButton1").addEventListener("click", ()=>switchActiveQuestion(1));
document.getElementById("questionImageButton2").addEventListener("click", ()=>switchActiveQuestion(2));
document.getElementById("questionImageButton3").addEventListener("click", ()=>switchActiveQuestion(3));
document.getElementById("questionImageButton4").addEventListener("click", ()=>switchActiveQuestion(4));

document.getElementById("cropDeleteButton1").addEventListener("click",()=>deleteCrop(1));
document.getElementById("cropDeleteButton2").addEventListener("click",()=>deleteCrop(2));
document.getElementById("cropDeleteButton3").addEventListener("click",()=>deleteCrop(3));
document.getElementById("cropDeleteButton4").addEventListener("click",()=>deleteCrop(4));

function resetCropper(){
  cropper.destroy();
  cropContainers = document.getElementsByClassName("finishedCrop");
  for (const crop of cropContainers){
    crop.src="";
  }
}

function deleteCrop(num) {
  for(let i = num; i<cropCount;i++){
    originalImages[String(i)]=originalImages[String(i+1)];
    resizedImages[String(i)]=resizedImages[String(i+1)];
    document.getElementById("finishedCrop"+i).src=document.getElementById("finishedCrop"+(i+1)).src;
  }
  document.getElementById("finishedCrop"+cropCount).src="";
  document.getElementById("cropDeleteButton"+cropCount).classList.add("hidden");
  delete originalImages[String(cropCount)];
  delete resizedImages[String(cropCount)];
  cropCount--;
  if (cropCount == 0){
    document.getElementById("submitCropButton").classList.add("inactiveDone");
  }
}
function switchActiveQuestion(num){
  if (document.getElementById("questionImageButton"+num).classList.contains("activeQuestion")) return;
  document.getElementsByClassName("activeQuestion")[0].classList.remove("activeQuestion");
  document.getElementById("questionImageButton"+num).classList.add("activeQuestion");
  document.getElementById("showImage").src=originalImages[String(num)];
  displayAnswers(Object.keys(sampleImageData[String(num)]));
  currQuestion=num;
  displaySampleImages(sampleImageData[String(currQuestion)], 0)
}

function prepareForSubsequentQuestion(){
  preds = document.getElementById("predictionTopBar").children;
  for (pred of preds){
    pred.classList.add("hidden");
  }
  document.getElementById("masterReferenceContainer").classList.add("hidden");
  document.getElementById("predContainer1").classList.remove("activePrediction");
}

function preloadImages(data){
  preloadedImages = []
  let keys;
  document.getElementById("preloadContainer").innerHTML="";
  for (let questionNum = 1; questionNum <= totalQuestions; questionNum++){
    keys = Object.keys(data[String(questionNum)]);
    console.log(keys);
    for (let i=0;i<5;i++){;
      console.log(i);
      for (const [index, fileName] of data[String(questionNum)][keys[i]].entries()){
        let uni='U+'+((keys[i].charCodeAt(0)).toString(16)).toUpperCase();
        var x = document.createElement("IMG");
        x.src='static\\samples\\'+uni+'\\'+fileName;
  
        document.getElementById("preloadContainer").appendChild(x);
      }
    }
  }
  
  
}

function displaySampleImages(data, idx){
  document.getElementById("masterReferenceContainer").style.animationPlayState="running";
  document.getElementById("masterReferenceContainer").classList.remove("hidden");
  let keys = Object.keys(data);
  for (const [index, fileName] of data[keys[idx]].entries()){
    let uni='U+'+((keys[idx].charCodeAt(0)).toString(16)).toUpperCase();
    console.log('samples\\'+uni+'\\'+fileName);
    let temp=document.getElementsByClassName("sampleImage"+(index+1))[0];
    temp.style.animationPlayState="running";
    temp.classList.remove("hidden");
    temp.src='static\\samples\\'+uni+'\\'+fileName;
  }
  //for (const key of keys){
  //  
  //}
}

function switchActiveAnswer (question, num){
  if (document.getElementById("pred"+num).innerHTML === "") return
  if (document.getElementById("predContainer"+num).classList.contains("activePrediction")) return

  for(let i=1; i<=5; i++){
    document.getElementById("predContainer"+i).classList.remove("activePrediction");
  }
  document.getElementById("predContainer"+num).classList.add("activePrediction");
  displaySampleImages(sampleImageData[String(currQuestion)], num-1);
}

function cropImage(){
  if (!(document.getElementById("pred1").innerHTML === "")){
    resetApp();
  }
  document.getElementById("cropPopupArea").classList.remove("hidden");
  img=document.getElementById("testImage");
  let image = document.getElementById("testImage");
    cropper = new Cropper(image, {
        autoCrop: false,
        viewMode: 2,
        movable: false,
        minContainerWidth: 0,
        highlight: false,
        ready(){
          cropper.setCanvasData({ height: img.clientHeight, width: img.clientWidth  });
        }
      
    });
  document.getElementById("file").value="";
}

function displayMatchHeader(){
  document.getElementById("predictionAreaHeader").style.animationPlayState="running";
  document.getElementById("horizontalBar").style.animationPlayState="running";
  document.getElementById("predictionAreaHeader").classList.remove("hidden");
  document.getElementById("horizontalBar").classList.remove("hidden");
}

function displayQuestionImage(){
  document.getElementById("dragAndDropLabel").style.display="none";
  document.getElementById("showImage").style.display="block";
  IMG_COUNT = Object.keys(resizedImages).length;
  for(let i=1;i<=IMG_COUNT;i++){
    document.getElementById("questionImageButton"+i).classList.remove("hidden", "activeQuestion");
  }
  document.getElementById("questionImageButton1").classList.add("activeQuestion");
}

function removePredictionPlaceholder(){
  document.getElementById("predictionAreaPlaceholder").classList.add("hidden");
  document.getElementById("predictionArea").classList.remove("hidden");
}

function displayAnswers(answerList){
  let i=1;
  for (const answer of answerList){
    let temp=document.getElementById("pred"+i);
    temp.innerHTML=answer;
    i++;
  }
  let predcontainers = document.getElementsByClassName("prediction");
  for(const element of predcontainers){
    element.style.animationPlayState="running";
    element.classList.remove("hidden");
  }
}

function resetApp(){
  resizedImages={};
  originalImages={};
  let questionImageButtons = document.getElementsByClassName("questionImageButton");
  for (const element of questionImageButtons){
    element.classList.add("hidden");
  }
  let deleteButtons = document.getElementsByClassName("cropDeleteButton");
  for (const element of deleteButtons){
    element.classList.add("hidden");
  }
  document.getElementById("submitCropButton").classList.add("inactiveDone");
}