const recSingerContainer=document.getElementById('recommendSinger');
window.addEventListener('DOMContentLoaded',function(){
    const img=document.createElement('img');
    img.src="../static/images/loading.gif";
    recSingerContainer.appendChild(img);
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/getRecommendSinger', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken',getCSRF());
    xhr.send();
    xhr.onreadystatechange=function(){
        if(xhr.readyState==4 && xhr.status == 200){
            recSingerContainer.innerHTML='';
            let recommendationData;
            recommendationData=JSON.parse(xhr.responseText);
            dynamicAppendSinger(recommendationData['data'],recSingerContainer);
            console.log(recommendationData['data']);
        }
    }
})
