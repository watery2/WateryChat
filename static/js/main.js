let msges = "";
let space = document.getElementById("space");
let tem = document.getElementsByTagName("template");
console.log(your_name)
var socket = io();
socket.on('connect', function(){
    socket.send({"msg": "Connected", "url": window.location.href});
});
socket.on('message', function(msg){
    let tem_clone1 = tem[0].content.cloneNode(true);
    let tem_clone2 = tem[1].content.cloneNode(true);
    if( msg.name === your_name){
        tem_clone2.querySelector(".your_msg").innerHTML = msg.msg ;
        space.appendChild(tem_clone2)
    }else{
        tem_clone1.querySelector(".msg").innerHTML = msg.name +": " + msg.msg ;
        space.appendChild(tem_clone1)
    }
    //msges = msges + msg + "<br>";
    //document.getElementById("msg").innerHTML = msges;
    console.log("msg");
});
document.getElementById("sendbutton").onclick = function(){
    socket.send({"msg": document.getElementById("msggs").value, "url": window.location.href});
    if(document.getElementById("msggs").value !== "Connected"){
        xhr = new XMLHttpRequest();
        xhr.open("POST", "/save");
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.send(JSON.stringify({"msg":document.getElementById("msggs").value, "room_name": room_name, "name": your_name}))
    }
    document.getElementById("msggs").value = "";

}