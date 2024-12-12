const recSongContainer=document.getElementById('recommendSong');
window.addEventListener('DOMContentLoaded',function(){
    const img=document.createElement('img');
    img.src="../static/images/loading.gif";
    recSongContainer.appendChild(img);
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/getRecommendation', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken',getCSRF());
    xhr.send();
    xhr.onreadystatechange=function(){
        if(xhr.readyState==4 && xhr.status == 200){
            recSongContainer.innerHTML='';
            let recommendationData;
            recommendationData=JSON.parse(xhr.responseText);
            dynamicAppendSong(recommendationData['recommendations'],recSongContainer,'item-song');
            //console.log(recommendationData['recommendations']);
        }
    }
})