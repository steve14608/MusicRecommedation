registerTab.addEventListener('click', () => {
    registerTab.classList.add('active');
    loginTab.classList.remove('active');
    registerForm.classList.add('active');
    loginForm.classList.remove('active');
});
registerForm.addEventListener('submit',function(event){
    event.preventDefault();
    const ensure = document.getElementById('ensure')
    const form = event.target;
    const formData = new FormData(form);
    const jso = Object.fromEntries(formData.entries())
    const jsonData = JSON.stringify(jso);
    if(jso['user_password'] !==ensure.value){
        alert("两次密码不一致，检查输入")
        return
    }
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/signup', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken',getCSRF());
    xhr.send(jsonData);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let json = JSON.parse(xhr.responseText);
            console.log(json);
            alert('注册成功！');
            location.reload();
        }
        else if(xhr.readyState===4){
            alert("该账号已被注册！")
        }
    };
})