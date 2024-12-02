const scrollContainer = document.getElementById('item-container');        
fetch('/getRecommend')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const items = data.items;
        console.log(items);
       items.forEach(item => {
           const listItem = document.createElement('li');
           const cover = document.createElement('img');
           cover.src=item.cover;
           cover.alt='';
           cover.onclick='play('+item.song_id+')';
           const songname = document.createElement('p');
           songname.textContent = item.song_name;
           listItem.appendChild(cover);
           listItem.appendChild(songname);
           scrollContainer.appendChild(listItem);
       });
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        //scrollContainer.innerHTML = '<li>Error loading items.</li>';
    });
// 鼠标拖拽滚动逻辑
// let isDragging = false; // 判断是否在拖拽
// let startX; // 鼠标按下时的起始位置
// let scrollLeft; // 初始滚动位置

// scrollContainer.addEventListener('mousedown', (e) => {
//     isDragging = true;
//     scrollContainer.classList.add('dragging');
//     startX = e.pageX - scrollContainer.offsetLeft;
//     scrollLeft = scrollContainer.scrollLeft;
// });

// scrollContainer.addEventListener('mouseleave', () => {
//     isDragging = false;
// });

// scrollContainer.addEventListener('mouseup', () => {
//     isDragging = false;
// });

// scrollContainer.addEventListener('mousemove', (e) => {
//     if (!isDragging) return;
//     e.preventDefault();
//     const x = e.pageX - scrollContainer.offsetLeft;
//     const walk = (x - startX) * 1.5; // 滚动距离，1.5 是滚动速度倍数
//     scrollContainer.scrollLeft = scrollLeft - walk;
// });