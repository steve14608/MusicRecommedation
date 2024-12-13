const audio = document.getElementById('audio');
const progressBar = document.querySelector('.progress');
const songCurrentTime=document.querySelector('.current-time');
const songEndTime=document.querySelector('.duration');
const displayButton=document.querySelector('.play-pause');
const prevButton=document.querySelector('.prev');
const nextButton=document.querySelector('.next');
const songCover = document.getElementById('cover');
const songName = document.getElementById('song-title');
const songSinger = document.getElementById('song-artist');
const recommendations = document.getElementById('recommendations');
const playPause = document.getElementById('play-pause');
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
    playPause.className = "fas fa-pause"
});
progressBar.addEventListener('input', (event) => {
    audio.currentTime = event.target.value;
});
displayButton.addEventListener('click', function () {
    if (playPause.className === "fas fa-play") {
        audio.play();
        playPause.className = "fas fa-pause"
    } else {
        audio.pause();
        playPause.className = "fas fa-play"
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

//动态添加歌曲
function dynamicAppendSong(Data,container,classname){
    Data.forEach(item => {
        const listItem = document.createElement('li');
        const cover = document.createElement('img');
        const songname = document.createElement('div');
        listItem.classList.add(classname);
        listItem.classList.add("item");
        cover.src=item.cover;
        cover.alt=item.song_name;
        cover.id=item.song_id;
        cover.onclick=function(){
            const jsData={
                'song_id':this.id
            };

            let xhr=new XMLHttpRequest;
            xhr.open('POST','/updateHistory',true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('X-CSRFToken',getCSRF());
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
            xhr1.send(JSON.stringify(jsData));
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
            xhr2.send(JSON.stringify(jsData));
            xhr2.onreadystatechange=function(){
                if(xhr2.readyState==4&&xhr2.status==200){
                    audio.src=xhr2.responseText;
                    audio.play();
                    playPause.className = "fas fa-pause"
                    // console.log(xhr2.responseText);
                }
            };
        
            let xhr3=new XMLHttpRequest;
            xhr3.open('POST','/getSong',true);
            xhr3.setRequestHeader('Content-Type', 'application/json');
            xhr3.setRequestHeader('X-CSRFToken',getCSRF());
            xhr3.send(JSON.stringify(jsData));
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
        listItem.classList.add('item-singer');
        listItem.classList.add("item");
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
                    handleSearchSubmit(event,songData['data'],songData['singer_name']);
                }
            }
            function handleSearchSubmit(event,Data,singer_name) {
                event.preventDefault(); 
                displaySearchResults(Data,singer_name); 
            }
            // 显示搜索结果的函数
            function displaySearchResults(Data,singer_name) {
                searchContent.innerHTML = '';
                var table = document.createElement('table');
                table.className = 'search-results-table'; 
                var thead = document.createElement('thead');
                var headerRow = document.createElement('tr');
                var headers = ['音乐名', '歌手',  '播放']; // 三列
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
                    //歌手列
                    var artistCell = document.createElement('td');
                    artistCell.textContent = singer_name;
                    row.appendChild(artistCell);
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
                        const jsData={
                            'song_id':this.id
                        };

                        let xhr=new XMLHttpRequest;
                        xhr.open('POST','/updateHistory',true);
                        xhr.setRequestHeader('Content-Type', 'application/json');
                        xhr.setRequestHeader('X-CSRFToken',getCSRF());
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
                        xhr1.send(JSON.stringify(jsData));
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
                        xhr2.send(JSON.stringify(jsData));
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
                        xhr3.send(JSON.stringify(jsData));
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