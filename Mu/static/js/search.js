let dataLength;
let res;
const searchResults = document.getElementById('searchResults');
const searchContent = document.getElementById('searchContent');
const searchForm=document.getElementById('search-form');
searchForm.addEventListener('submit',function(event){
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const jsonData = JSON.stringify(Object.fromEntries(formData.entries()));
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/searchSong', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken',getCSRF())
    xhr.send(jsonData);
    xhr.onreadystatechange=function(){
        if(xhr.readyState==4&&xhr.status==200){
            let json=JSON.parse(xhr.responseText);
            let jsonReturnData=json['data'];
            dataLength=jsonReturnData.length;
            console.log(jsonReturnData);
            handleSearchSubmit(event,jsonReturnData);
        }
        else if(xhr.readyState==4){
            alert('请重新输入您要搜索的内容')
        }
    }
    
});
function handleSearchSubmit(event,jsonReturnData) {
    event.preventDefault(); 
    displaySearchResults(jsonReturnData); 
}
// 显示搜索结果的函数
function displaySearchResults(jsonReturnData) {
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
    for(i=0;i<dataLength;i++){
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
        titleSpan.textContent = jsonReturnData[i].song_name;
        titleCell.appendChild(titleSpan);
        row.appendChild(titleCell);
        // 歌手列
        var artistCell = document.createElement('td');
        artistCell.textContent = jsonReturnData[i].song_singer;
        row.appendChild(artistCell);
        // 专辑列
        var albumCell = document.createElement('td');
        albumCell.textContent = jsonReturnData[i].song_album;
        row.appendChild(albumCell);
        // 时长列
        var durationCell = document.createElement('td');
        durationCell.textContent = formatTime(jsonReturnData[i].song_duration / 1000);
        row.appendChild(durationCell);
        //加按钮
        var playCell = document.createElement('td');
        var playButton = document.createElement('button');
        playButton.textContent = '播放';
        playButton.className='playSong';
        playButton.id=jsonReturnData[i].song_id;
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
    document.querySelector('.recommendations').style.display = 'none';
}


