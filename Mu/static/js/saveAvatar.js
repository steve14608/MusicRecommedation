const avatarForm=document.getElementById('avatarForm');
const avatar=document.getElementById('avatar');
let xhr = new XMLHttpRequest();
xhr.open('POST', '/getUserAvatar', true);
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.setRequestHeader('X-CSRFToken',getCSRF());
xhr.send();
console.log(xhr.response);
function handleFiles(files) {
    if (files.length > 0) {
        let file = files[0]; 
        let reader = new FileReader();
        reader.onload = function(e) {
            let imgElement = document.getElementById('avatar'); 
            imgElement.src = e.target.result;
        };
        reader.readAsDataURL(file); 
        const formData = new FormData();
        if(file) console.log("A")
        formData.append('avatar', file);
        fetch('/updateAvatar',{
            'method':'POST',
            'body':formData,
            'headers':{
                'X-CSRFToken':getCSRF()
            }
        })
    }
}
