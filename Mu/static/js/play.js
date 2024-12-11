const scrollContainer=document.querySelectorAll('item-container');
const audio = document.getElementById('audio');
const lyricontent=document.getElementById('lyrics');
const progressBar = document.querySelector('.progress');
const songCurrentTime=document.querySelector('.current-time');
const songEndTime=document.querySelector('.duration');
const displayButton=document.querySelector('.play-pause');
const prevButton=document.querySelector('.prev');
const nextButton=document.querySelector('.next');
const songCover = document.getElementById('cover');
const songName = document.getElementById('song-title');
const songSinger = document.getElementById('song-artist');
const searchResults = document.getElementById('searchResults');
const searchContent = document.getElementById('searchContent');
const recommendations = document.getElementById('recommendations');
let lyricArray=[];
let cur;
let isDragging; 
let startX;
let scrollLeft;
audio.addEventListener('timeupdate',function(){
    let curTime=audio.currentTime;
    console.log(curTime);
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
scrollContainer.forEach(item =>{
    isDragging=false;
    item.addEventListener('mousedown', (e) => {
        isDragging = true;
        item.classList.add('dragging');
        startX = e.pageX - item.offsetLeft;
        scrollLeft = item.scrollLeft;
    });
    item.addEventListener('mouseleave', () => {
        isDragging = false;
    });
    item.addEventListener('mouseup', () => {
        isDragging = false;
    });
    item.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        e.preventDefault();
        const x = e.pageX - item.offsetLeft;
        const walk = (x - startX) * 1.5; // 滚动距离，1.5 是滚动速度倍数
        item.scrollLeft = scrollLeft - walk;
    });
})
//动态添加歌曲
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
                    let lyrics=data['lyrics'];
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
//推荐歌手
function dynamicAppendSinger(Data,container){
    Data.forEach(item => {
        const listItem = document.createElement('li');
        const cover = document.createElement('img');
        const singername = document.createElement('div');
        listItem.classList.add('item');
        cover.src=item.singer_pic;
        cover.alt=item.singer_name;
        cover.id=item.singer_id;
        cover.onclick=function(){
            let request=new XMLHttpRequest();
            request.open("POST","/getSongBySingerId",true);
            request.setRequestHeader('Content-Type', 'application/json');
            request.setRequestHeader('X-CSRFToken',getCSRF());
            request.send(JSON.stringify({'song_singer_id':this.id}));
            request.onreadystatechange=function(){
                if(request.readyState==4 && request.status==200){
                    let songData=JSON.parse(request.responseText);
                    handleSearchSubmit(event,songData['data']);
                    console.log(songData['data']);
                }
            }
            function handleSearchSubmit(event,Data) {
                event.preventDefault(); 
                displaySearchResults(Data); 
            }
            // 显示搜索结果的函数
            function displaySearchResults(Data) {
                searchContent.innerHTML = '';
                var table = document.createElement('table');
                table.className = 'search-results-table'; 
                var thead = document.createElement('thead');
                var headerRow = document.createElement('tr');
                var headers = ['音乐名', '歌手', '专辑', '时长', '播放']; // 五列
                for(i=0;i<headers.length;i++){
                    var header = document.createElement('th');
                    header.textContent = headers[i];
                    header.style.color = '#666'; 
                    headerRow.appendChild(header);
                }
                thead.appendChild(headerRow);
                table.appendChild(thead);
                var tbody = document.createElement('tbody');
                // 填充表格数据
                for(i=0;i<Data.length;i++){
                    var row = document.createElement('tr');
                    // 封面与音乐标题列
                    // var coverImg = document.createElement('img');
                    // if(i<dataLength){
                    //     coverImg.src = jsonReturnData[i].cover; // 假设result对象中有cover属性
                    //     coverImg.style.width = '50px'; // 设置封面图片宽度
                    //     coverImg.style.marginRight = '10px'; // 在封面和标题之间添加一些间距
                    //     titleCell.appendChild(coverImg);
                    // }
                    var titleCell = document.createElement('td');
                    var titleSpan = document.createElement('span');
                    titleSpan.textContent = Data[i].song_name;
                    titleCell.appendChild(titleSpan);
                    row.appendChild(titleCell);
                    // 歌手列
                    // var artistCell = document.createElement('td');
                    // artistCell.textContent = jsonReturnData[i].song_singer;
                    // row.appendChild(artistCell);
                    // 专辑列
                    // var albumCell = document.createElement('td');
                    // albumCell.textContent = jsonReturnData[i].song_album;
                    // row.appendChild(albumCell);
                    // 时长列
                    // var durationCell = document.createElement('td');
                    // durationCell.textContent = formatTime(jsonReturnData[i].song_duration / 1000);
                    // row.appendChild(durationCell);
                    //加按钮
                    var playCell = document.createElement('td');
                    var playButton = document.createElement('button');
                    playButton.textContent = '播放';
                    playButton.className='playSong';
                    playButton.id=Data[i].song_id;
                    playButton.onclick=function(){
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
                        console.log("fuck1");
                        xhr1.onreadystatechange=function(){
                            if(xhr1.readyState==4&&xhr1.status==200){
                                lyricArray = [];
                                cur = 0;
                                let data=JSON.parse(xhr1.responseText);
                                let lyrics=data['lyrics'];
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
                    playCell.appendChild(playButton);
                    row.appendChild(playCell);
                    console.log(row);
                    // 将行添加到表体
                    tbody.appendChild(row);
                }
                // 将表体添加到表格
                table.appendChild(tbody);
            
                const div=document.createElement('div');
                div.style.height="100px";
                // 将表格添加到搜索结果内容
                searchContent.appendChild(table);
                searchContent.appendChild(div);
            
                // 显示搜索结果容器，隐藏其他内容
                searchResults.style.display = 'block';
                recommendations.style.display = 'none';
            }
        }
        singername.textContent=item.singer_name;
        listItem.appendChild(cover);
        listItem.appendChild(singername); 
        container.appendChild(listItem);
    });
}
// 返回到主内容的函数
function backToMainContent() {        
    searchResults.style.display = 'none';
    recommendations.style.display = 'block';

}
//处理时间
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
}