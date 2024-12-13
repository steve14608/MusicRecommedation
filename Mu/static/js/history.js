const historyContainer=document.getElementById('songHistory');
window.addEventListener('DOMContentLoaded',function(){
    const img=document.createElement('img');
    img.src="../static/images/loading.gif";
    historyContainer.appendChild(img);
    function XHRsend(){
        let xhr = new XMLHttpRequest();
        xhr.open('POST', '/getHistory', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('X-CSRFToken',getCSRF());
        xhr.send();
        xhr.onreadystatechange=function(){
            if(xhr.readyState==4 && xhr.status == 200){
                historyContainer.innerHTML='';
                let historyData;
                historyData=JSON.parse(xhr.responseText);
                dynamicAppendSong(historyData['items'],historyContainer,'item-history');
            }
        }   
    }
    this.setInterval(XHRsend,15000);
    
})