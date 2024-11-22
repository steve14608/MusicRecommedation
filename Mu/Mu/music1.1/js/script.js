document.querySelector('.play-pause').addEventListener('click', function () {
    let button = this;
    if (button.textContent === '⏯') {
        button.textContent = '⏸'; // 切换为暂停
    } else {
        button.textContent = '⏯'; // 切换为播放
    }
});

document.querySelector('.prev').addEventListener('click', function () {
    alert('上一首歌');
});

document.querySelector('.next').addEventListener('click', function () {
    alert('下一首歌');
});

// 当文件输入字段变化时触发的函数
function handleFiles(files) {
    if (files.length > 0) {
        var file = files[0]; // 获取选择的第一个文件，通常是用户选择的图片
        var reader = new FileReader(); // 创建FileReader对象
        
        reader.onload = function(e) {
            // 当文件读取完成时触发
            var imgElement = document.getElementById('avatar'); // 获取<img>元素
            imgElement.src = e.target.result; // 设置<img>的src属性为读取的结果，显示图片
        };
        
        reader.readAsDataURL(file); // 以DataURL的形式读取文件内容
    }
}