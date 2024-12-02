const historyContainer=document.querySelectorAll('item-container')[2]
let jsonReturnData;
window.addEventListener('DOMContentLoaded',function(event){
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/getHistory', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken',getCSRF())
    xhr.send();
    xhr.onreadystatechange=function(){
        if(xhr.readyState==4 && xhr.status == 200){
            jsonReturnData=JSON.parse(xhr.responseText());
            console.log(jsonReturnData);
        }
        else{
            alert('错误')
        }
    }
    // jsonReturnData.forEach(item => {
    //     const listItem = document.createElement('div');
    //     const cover = document.createElement('img');
    //     cover.src=item.cover;
    //     cover.alt='';
    //     cover.onclick='play('+item.song_id+')'; 
    //     const songname = document.createElement('p');
    //     songname.textContent = item.song_name;  
    //     listItem.appendChild(cover);
    //     listItem.appendChild(songname);  
    //     historyContainer.appendChild(listItem);
    // });
})
// fetch('/api/history/')
//             .then(response => {
//                 if (!response.ok) {
//                     throw new Error('Network response was not ok');
//                 }
//                 return response.json();
//             })
//             .then(data => {
//                 const items = data.items;
//                 items.forEach(item => {
//                     const listItem = document.createElement('li');

//                     const cover = document.createElement('img');
//                     cover.src=item.cover;
//                     cover.alt='';
//                     cover.onclick='play('+item.song_id+')';

//                     const songname = document.createElement('p');
//                     songname.textContent = item.song_name;

//                     listItem.appendChild(cover);
//                     listItem.appendChild(songname);

//                     historyContainer.appendChild(listItem);
//                 });
//             })
//             .catch(error => {
//                 console.error('Error fetching data:', error);
//                 //scrollContainer.innerHTML = '<li>Error loading items.</li>';
//             });

        // 鼠标拖拽滚动逻辑
let isDragging = false; 
let startX; // 鼠标按下时的起始位置
let scrollLeft; // 初始滚动位置
historyContainer.addEventListener('mousedown', (e) => {
    isDragging = true;
    historyContainer.classList.add('dragging');
    startX = e.pageX - historyContainer.offsetLeft;
    scrollLeft = historyContainer.scrollLeft;
});
historyContainer.addEventListener('mouseleave', () => {
    isDragging = false;
});
historyContainer.addEventListener('mouseup', () => {
    isDragging = false;
});
historyContainerhistoryContainer.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    e.preventDefault();
    const x = e.pageX - historyContainer.offsetLeft;
    const walk = (x - startX) * 1.5; // 滚动距离，1.5 是滚动速度倍数
    historyContainer.scrollLeft = scrollLeft - walk;
});