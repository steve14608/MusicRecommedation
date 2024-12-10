const recSingerContainer=document.getElementById('recommendSinger');
window.addEventListener('DOMContentLoaded',function(){
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/getRecommendSinger', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken',getCSRF());
    xhr.send();
    xhr.onreadystatechange=function(){
        if(xhr.readyState==4 && xhr.status == 200){
            console.log
            let recommendatinData;
            recommendatinData=JSON.parse(xhr.responseText);
            // dynamicAppendSinger(recommendatinData['data'],recSongContainer);
            console.log(recommendatinData['data']);
        }
    }
})