let jsonReturnData;
let dataLength;
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
            jsonReturnData=json['data'];
            dataLength=jsonReturnData.length;
            console.log(jsonReturnData);
            document.querySelector('.search-form').addEventListener('submit', handleSearchSubmit(event,jsonReturnData));
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
    var searchResults = document.getElementById('searchResults');
    var searchContent = document.getElementById('searchContent');
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
        var titleCell = document.createElement('td');
        var coverImg = document.createElement('img');
        coverImg.src = jsonReturnData[i].cover; // 假设result对象中有cover属性
        coverImg.style.width = '50px'; // 设置封面图片宽度
        coverImg.style.marginRight = '10px'; // 在封面和标题之间添加一些间距
        titleCell.appendChild(coverImg);
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
        albumCell.textContent = ' ';
        row.appendChild(albumCell);
        // 时长列
        var durationCell = document.createElement('td');
        durationCell.textContent = ' ';
        row.appendChild(durationCell);
        // 播放按钮列
        var playCell = document.createElement('td');
        var playButton = document.createElement('button');
        playButton.textContent = '播放';
        playButton.onclick = function() {};
        playCell.appendChild(playButton);
        row.appendChild(playCell);
        // 将行添加到表体
        tbody.appendChild(row);
    }
    // 将表体添加到表格
    table.appendChild(tbody);
    // 将表格添加到搜索结果内容
    searchContent.appendChild(table);
    // 显示搜索结果容器，隐藏其他内容
    searchResults.style.display = 'block';
    document.querySelector('.recommendations').style.display = 'none';
}
// 返回到主内容的函数
function backToMainContent() {
    var searchResults = document.getElementById('searchResults');
    var recommendations = document.querySelector('.recommendations');
    // 隐藏搜索结果容器，显示原始内容
    searchResults.style.display = 'none';
    recommendations.style.display = 'block';
}
// 绑定搜索表单的提交事件

// const items = jsonReturnData.items;
// items.forEach(item => {
//     const listItem = document.createElement('li');
//     const cover = document.createElement('img');
//     cover.src=item.cover;
//     cover.alt='';
//     cover.onclick='play('+item.song_id+')';
//     const songname = document.createElement('p');
//     songname.textContent = item.song_na
//     listItem.appendChild(cover);
//     listItem.appendChild(songname);
//     historyContainer.appendChild(listItem);
// });