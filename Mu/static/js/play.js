const scrollContainer=document.querySelectorAll('item-container');
let isDragging = false; 
let startX;
let scrollLeft;
//处理监听
audio.addEventListener('timeupdate',function(){
    let curTime=audio.currentTime;
    render(curTime);
})
audio.addEventListener('timeupdate', ()=>{
    songCurrentTime.textContent=formatTime(audio.currentTime);
    progressBar.value = audio.currentTime;
});
audio.addEventListener('loadedmetadata', () => {
    songEndTime.textContent = formatTime(audio.duration);
    progressBar.max = audio.duration; 
});
audio.addEventListener('ended', () => {
    displayButton.textContent='⏯';
});
progressBar.addEventListener('input', (event) => {
    audio.currentTime = event.target.value;
});
displayButton.addEventListener('click', function () {
    if (this.textContent === '⏯') {
        audio.play();
        this.textContent = '⏸'; 
    } else {
        audio.pause();
        this.textContent = '⏯'; 
    }
});
prevButton.addEventListener('click', function () {
    if(audio.currentTime>=5){
        audio.currentTime=audio.currentTime-5;
    }
});

nextButton.addEventListener('click', function () {
    audio.currentTime=audio.currentTime+5;
});
//处理歌词
function processLyric(lyric) {
    for (let i of lyric.split('\n')) {
        if(i.charAt(0) == '['){
            let tempa = i.substring(i.indexOf('[') + 1, i.lastIndexOf(']')).split(':');
            let ttime = parseInt(tempa[0]) * 60 + parseFloat(tempa[1]);
            lyricArray.push({ 'time': ttime, 'content': i.slice(i.indexOf(']') + 1) });
        }
        else continue;
    }
}

function locate(curtime, le, ri) {
    while (le < ri) {
        console.log(le)
        console.log(ri)
        let mid = parseInt((le + ri) / 2);
        if (lyricArray[mid].time == curtime) {
            cur = mid;
            return;
        }
        else if (lyricArray[mid].time > curtime) {
            ri = mid ;
        }
        else {
            if (lyricArray[mid + 1].time > curtime) {
                cur = mid;
                return;
            }
            le = mid + 1;
        }
    }
}

function render(curtime) {
    if (lyricArray.length == 0) return;
    if (curtime < lyricArray[cur].time || cur < lyricArray.length - 2 && curtime > lyricArray[cur + 2].time) {
        if (curtime < lyricArray[cur].time) locate(curtime, 0, cur);
        else locate(curtime, cur, lyricArray.length - 1);
    }
    else if (cur == lyricArray.length - 1 || curtime < lyricArray[cur + 1].time) return;
    else {
        ++cur;
    }
    if(lyricArray[cur].content.length>=64){
        console.log('执行');
        lyricontent.textContent=lyricArray[cur].content.slice(0,64)+'......';
    }
    else lyricontent.textContent = lyricArray[cur].content;
}
//鼠标拖拽
scrollContainer.addEventListener('mousedown', (e) => {
    isDragging = true;
    scrollContainer.classList.add('dragging');
    startX = e.pageX - scrollContainer.offsetLeft;
    scrollLeft = scrollContainer.scrollLeft;
});
scrollContainer.addEventListener('mouseleave', () => {
    isDragging = false;
});
scrollContainer.addEventListener('mouseup', () => {
    isDragging = false;
});
scrollContainer.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    e.preventDefault();
    const x = e.pageX - scrollContainer.offsetLeft;
    const walk = (x - startX) * 1.5; // 滚动距离，1.5 是滚动速度倍数
    scrollContainer.scrollLeft = scrollLeft - walk;
});
//动态添加列表
function dynamicAppendSong(Data,container){
    Data.forEach(item => {
        const listItem = document.createElement('li');
        const cover = document.createElement('img');
        const songname = document.createElement('div');
        listItem.classList.add('item');
        cover.src=item.cover;
        cover.alt=item.song_name;
        cover.id=item.song_id;
        cover.onclick=function(){
            let xhr=new XMLHttpRequest;
            xhr.open('POST','/updateHistory',true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('X-CSRFToken',getCSRF());
            const jsData={
                'song_id':this.id
            };
            xhr.send(JSON.stringify(jsData));
            xhr.onreadystatechange=function(){
                if(xhr.readyState==4&&xhr.status==200){
                    console.log('更新完成');
                }
            };
        
            let xhr1=new XMLHttpRequest;
            xhr1.open('POST','/getSongLyrics',true);
            xhr1.setRequestHeader('Content-Type', 'application/json');
            xhr1.setRequestHeader('X-CSRFToken',getCSRF());
            const jsData1={
                'song_id':this.id
            };
            xhr1.send(JSON.stringify(jsData1));
            xhr1.onreadystatechange=function(){
                if(xhr1.readyState==4&&xhr1.status==200){
                    lyricArray = [];
                    cur = 0;
                    let data=JSON.parse(xhr1.responseText);
                    let lyrics=data['lyric'];
                    processLyric(lyrics);
                    // console.log(lyricArray);
                }
            };
        
            let xhr2=new XMLHttpRequest;
            xhr2.open('POST','/getSongUrl',true);
            xhr2.setRequestHeader('Content-Type', 'application/json');
            xhr2.setRequestHeader('X-CSRFToken',getCSRF());
            const jsData2={
                'song_id':this.id
            };
            xhr2.send(JSON.stringify(jsData2));
            xhr2.onreadystatechange=function(){
                if(xhr2.readyState==4&&xhr2.status==200){
                    audio.src=xhr2.responseText;
                    audio.play();
                    displayButton.textContent='⏸';
                    // console.log(xhr2.responseText);
                }
            };
        
            let xhr3=new XMLHttpRequest;
            xhr3.open('POST','/getSong',true);
            xhr3.setRequestHeader('Content-Type', 'application/json');
            xhr3.setRequestHeader('X-CSRFToken',getCSRF());
            const jsData3={
                'song_id':this.id
            };
            xhr3.send(JSON.stringify(jsData3));
            xhr3.onreadystatechange=function(){
                if(xhr3.readyState==4&&xhr3.status==200){
                    let Data=JSON.parse(xhr3.responseText);
                    songName.textContent=Data['song_name'];
                    songCover.src=Data['cover'];
                    songSinger.textContent=Data['singer'];
                    // console.log(Data['cover'])
                    // console.log(Data);
                }
            };
        }
        songname.textContent=item.song_name;
        listItem.appendChild(cover);
        listItem.appendChild(songname); 
        container.appendChild(listItem);
    });
}
function clickToplay(){

}