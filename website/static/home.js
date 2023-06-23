//<div class="tooltipAlert">!</div>
//<div class="tooltipText">This kanji is the old form of 口</div>
var socket = io();
let cropper;
let kyuujitaiDict = {'亞': '亜', '惡': '悪', '壓': '圧', '圍': '囲', '爲': '為', '醫': '医', '壹': '壱', '稻': '稲', '飮': '飲', '隱': '隠', '羽': '羽', '營': '営', '榮': '栄', '衞': '衛', '益': '益', '驛': '駅', '悅': '悦', '圓': '円', '艷': '艶', '鹽': '塩', '奧': '奥', '應': '応', '橫': '横', '歐': '欧', '毆': '殴', '穩': '穏', '假': '仮', '價': '価', '畫': '画', '會': '会', '囘': '回', '懷': '懐', '繪': '絵', '擴': '拡', '殼': '殻', '覺': '覚', '學': '学', '嶽': '岳', '樂': '楽', '勸': '勧', '卷': '巻', '寬': '寛', '歡': '歓', '罐': '缶', '觀': '観', '閒': '間', '關': '関', '陷': '陥', '館': '館', '巖': '巌', '顏': '顔', '歸': '帰', '氣': '気', '龜': '亀', '僞': '偽', '戲': '戯', '犧': '犠', '卻': '却', '糺': '糾', '舊': '旧', '據': '拠', '擧': '挙', '峽': '峡', '挾': '挟', '敎': '教', '狹': '狭', '鄕': '郷', '堯': '尭', '曉': '暁', '區': '区', '驅': '駆', '勳': '勲', '薰': '薫', '羣': '群', '徑': '径', '惠': '恵', '攜': '携', '溪': '渓', '經': '経', '繼': '継', '莖': '茎', '螢': '蛍', '輕': '軽', '鷄': '鶏', '藝': '芸', '缺': '欠', '儉': '倹', '劍': '剣', '圈': '圏', '檢': '検', '權': '権', '獻': '献', '縣': '県', '險': '険', '顯': '顕', '驗': '験', '嚴': '厳', '效': '効', '廣': '広', '恆': '恒', '鑛': '鉱', '號': '号', '國': '国', '黑': '黒', '濟': '済', '碎': '砕', '齋': '斎', '劑': '剤', '冱': '冴', '櫻': '桜', '册': '冊', '雜': '雑', '參': '参', '慘': '惨', '棧': '桟', '蠶': '蚕', '贊': '賛', '殘': '残', '絲': '糸', '飼': '飼', '齒': '歯', '兒': '児', '辭': '辞', '濕': '湿', '實': '実', '舍': '舎', '寫': '写', '釋': '釈', '壽': '寿', '收': '収', '從': '従', '澁': '渋', '獸': '獣', '縱': '縦', '肅': '粛', '處': '処', '緖': '緒', '諸': '諸', '敍': '叙', '奬': '奨', '將': '将', '牀': '床', '燒': '焼', '祥': '祥', '稱': '称', '證': '証', '乘': '乗', '剩': '剰', '壤': '壌', '孃': '嬢', '條': '条', '淨': '浄', '疊': '畳', '穰': '穣', '讓': '譲', '釀': '醸', '囑': '嘱', '觸': '触', '寢': '寝', '愼': '慎', '晉': '晋', '眞': '真', '神': '神', '刄': '刃', '盡': '尽', '圖': '図', '粹': '粋', '醉': '酔', '隨': '随', '髓': '髄', '數': '数', '樞': '枢', '瀨': '瀬', '晴': '晴', '淸': '清', '精': '精', '靑': '青', '聲': '声', '靜': '静', '齊': '斉', '蹟': '跡', '攝': '摂', '竊': '窃', '專': '専', '戰': '戦', '淺': '浅', '潛': '潜', '纖': '繊', '踐': '践', '錢': '銭', '禪': '禅', '曾': '曽', '雙': '双', '壯': '壮', '搜': '捜', '插': '挿', '爭': '争', '窗': '窓', '總': '総', '聰': '聡', '莊': '荘', '裝': '装', '騷': '騒', '增': '増', '臟': '臓', '藏': '蔵', '屬': '属', '續': '続', '墮': '堕', '體': '体', '對': '対', '帶': '帯', '滯': '滞', '臺': '台', '瀧': '滝', '擇': '択', '澤': '沢', '單': '単', '擔': '担', '膽': '胆', '團': '団', '彈': '弾', '斷': '断', '癡': '痴', '遲': '遅', '晝': '昼', '蟲': '虫', '鑄': '鋳', '猪': '猪', '廳': '庁', '聽': '聴', '敕': '勅', '鎭': '鎮', '塚': '塚', '遞': '逓', '鐵': '鉄', '轉': '転', '點': '点', '傳': '伝', '都': '都', '黨': '党', '盜': '盗', '燈': '灯', '當': '当', '鬪': '闘', '德': '徳', '獨': '独', '讀': '読', '屆': '届', '繩': '縄', '貳': '弐', '姙': '妊', '黏': '粘', '惱': '悩', '腦': '脳', '霸': '覇', '廢': '廃', '拜': '拝', '賣': '売', '麥': '麦', '發': '発', '髮': '髪', '拔': '抜', '飯': '飯', '蠻': '蛮', '祕': '秘', '濱': '浜', '甁': '瓶', '福': '福', '拂': '払', '佛': '仏', '竝': '並', '變': '変', '邊': '辺', '邉': '辺', '辨': '弁', '辯': '弁', '瓣': '弁', '舖': '舗', '穗': '穂', '寶': '宝', '萠': '萌', '襃': '褒', '豐': '豊', '沒': '没', '飜': '翻', '槇': '槙', '萬': '万', '滿': '満', '默': '黙', '餠': '餅', '彌': '弥', '藥': '薬', '譯': '訳', '藪': '薮', '豫': '予', '餘': '余', '與': '与', '譽': '誉', '搖': '揺', '樣': '様', '謠': '謡', '遙': '遥', '瑤': '瑶', '慾': '欲', '來': '来', '賴': '頼', '亂': '乱', '覽': '覧', '畧': '略', '隆': '隆', '龍': '竜', '兩': '両', '獵': '猟', '綠': '緑', '鄰': '隣', '凛': '凜', '壘': '塁', '勵': '励', '禮': '礼', '隸': '隷', '靈': '霊', '齡': '齢', '戀': '恋', '爐': '炉', '勞': '労', '朗': '朗', '樓': '楼', '郞': '郎', '祿': '禄', '亙': '亘', '灣': '湾'};
let kyuujitaiKeys =Object.keys(kyuujitaiDict);
let sampleImageData;
let preloadedImages = [];
let cropCount=0;
let totalQuestions;
let currQuestion;
let resizedImages = {};
let originalImages = {};
socket.on("answer", function(data){
  sampleImageData=data;
  totalQuestions=(Object.keys(data)).length;
  currQuestion=1;
  preloadImages(sampleImageData);
  document.getElementById("loadingContainer").classList.add("hidden");
  displayAnswers(Object.keys(data["1"]));
  switchActiveAnswer(1,1);
});

document.getElementById("addCropButton").addEventListener("click", ()=>{
  document.getElementById("submitCropButton").classList.remove("inactiveDone");
  cropCount++;
  let img = document.getElementById("finishedCrop"+(cropCount));
  document.getElementById("cropDeleteButton"+cropCount).classList.remove("hidden");
  if (Object.keys(cropper.getCropBoxData()).length === 0){
    let data={
      left: 0,
      right: 0,
      width: cropper.getImageData().width,
      height: cropper.getImageData().height
    };
    cropper.crop();
    cropper.setCropBoxData(data);
  }
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
  if(cropCount==4){
    document.getElementById("loadingContainer").classList.remove("hidden");
    document.getElementById("loadingContainer").style.animationPlayState="running";
  }
  cropCount=0;
  
});

document.getElementById("predContainer1").addEventListener("click",()=>switchActiveAnswer(currQuestion, 1));
document.getElementById("predContainer2").addEventListener("click",()=>switchActiveAnswer(currQuestion, 2));
document.getElementById("predContainer3").addEventListener("click",()=>switchActiveAnswer(currQuestion, 3));
document.getElementById("predContainer4").addEventListener("click",()=>switchActiveAnswer(currQuestion, 4));
document.getElementById("predContainer5").addEventListener("click",()=>switchActiveAnswer(currQuestion, 5));

document.getElementById("questionImageButton1").addEventListener("click", ()=>switchActiveQuestion(1));
document.getElementById("questionImageButton2").addEventListener("click", ()=>switchActiveQuestion(2));
document.getElementById("questionImageButton3").addEventListener("click", ()=>switchActiveQuestion(3));
document.getElementById("questionImageButton4").addEventListener("click", ()=>switchActiveQuestion(4));

document.getElementById("cropDeleteButton1").addEventListener("click",()=>deleteCrop(1));
document.getElementById("cropDeleteButton2").addEventListener("click",()=>deleteCrop(2));
document.getElementById("cropDeleteButton3").addEventListener("click",()=>deleteCrop(3));
document.getElementById("cropDeleteButton4").addEventListener("click",()=>deleteCrop(4));

document.getElementById("demoButton").addEventListener("click", ()=>{
  document.getElementById("testImage").src='static\\demoImage.png';
  cropImage();
});

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
  document.getElementsByClassName("activePrediction")[0].classList.remove("activePrediction");
  document.getElementById("predContainer1").classList.add("activePrediction");
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
  document.getElementById("loadingContainer").style.animationDelay="0s";
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
  img=document.getElementById("testImage");
  let image = document.getElementById("testImage");
  document.getElementById("file").value="";
  cropper = new Cropper(image, {
      autoCrop: false,
      viewMode: 2,
      movable: false,
      minContainerWidth: 0,
      minContainerHeight: 200,
      highlight: false,
      ready(){
      }
  });
  document.getElementById("cropPopupArea").classList.remove("hidden");
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
  if(IMG_COUNT == 1){
    return;
  }
  for(let i=1;i<=IMG_COUNT;i++){
    document.getElementById("questionImageButton"+i).classList.remove("hidden");
  }
  document.getElementById("questionImageButton1").classList.add("activeQuestion");
  document.getElementById("questionImageButton"+IMG_COUNT).classList.add("finalQuestion");
}

function removePredictionPlaceholder(){
  document.getElementById("predictionAreaPlaceholder").classList.add("hidden");
  document.getElementById("predictionArea").classList.remove("hidden");
}

function displayAnswers(answerList){
  removeTooltips();
  let i=1;
  for (const answer of answerList){
    let temp=document.getElementById("pred"+i);
    temp.innerHTML=answer;
    if (kyuujitaiKeys.includes(answer)){
      addTooltip(i, answer);
    }
    i++;
  }
  let predcontainers = document.getElementsByClassName("prediction");
  for(const element of predcontainers){
    element.style.animationPlayState="running";
    element.classList.remove("hidden");
  }
}

function addTooltip (index, kanji){
  let container = document.getElementById("predContainer"+index);
  let newkanji = kyuujitaiDict[kanji];
  let alertdiv = document.createElement("div");
  let alerttxt = document.createTextNode("!");
  alertdiv.appendChild(alerttxt);
  let tooltip = document.createElement("div");
  let tooltiptext = document.createTextNode("This kanji is the old form of "+newkanji);
  tooltip.appendChild(tooltiptext);

  alertdiv.classList.add("tooltipAlert");
  tooltip.classList.add("tooltipText");

  container.appendChild(alertdiv);
  container.appendChild(tooltip);
}

function removeTooltips(){
  let tooltipelements = (document.getElementsByClassName("tooltipAlert"));
  for (const element of tooltipelements){
    element.remove();
  }
  tooltipelements = document.getElementsByClassName("tooltipText");
  for (const element of tooltipelements){
    element.remove();
  }
}

function resetApp(){
  resizedImages={};
  originalImages={};
  let questionImageButtons = document.getElementsByClassName("questionImageButton");
  for (const element of questionImageButtons){
    element.classList.add("hidden");
    element.classList.remove("activeQuestion");
    element.classList.remove("finalQuestion");
  }
  let deleteButtons = document.getElementsByClassName("cropDeleteButton");
  for (const element of deleteButtons){
    element.classList.add("hidden");
  }
  document.getElementById("submitCropButton").classList.add("inactiveDone");
}