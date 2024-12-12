const logoutButton=document.getElementById('logout')
logoutButton.onclick=function(){
    document.cookie = "user_id=0";
    location.reload();
}