const form = document.getElementById('userInfoForm')
const nickname = document.getElementById('nickname')
const signature = document.getElementById('signature')
//页面加载时执行显示用户信息（不包括图像）
window.addEventListener('DOMContentLoaded',function(){
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/getUserDetail', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken',getCSRF());
    xhr.send();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let json = JSON.parse(xhr.responseText);
            console.log(json);
            nickname.value=json['user_nickname'];
            signature.value=json['user_bio'];
        }
    }; 
     
})
//更新消息
form.addEventListener('submit',function(event){
    event.preventDefault();
    const jsonData = {"user_nickname":nickname.value,"user_bio":signature.value};
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/updateInfo', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken',getCSRF());
    xhr.send(JSON.stringify(jsonData));
})