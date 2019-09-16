// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.
import { XMLHttpRequest } from 'xmlhttprequest-ts';

function processResponse(response: any) {
    console.log(response);
}

var ipc = require('electron').ipcRenderer;
var authButton = document.getElementById('about');
authButton.addEventListener('click', function(){
    ipc.once('actionReply', function(event: any, response: any){
        processResponse(response);
    })
    ipc.send('invokeAction', 'data to main process');

    var request = new XMLHttpRequest();
    request.open('post', 'http://127.0.0.1:5000/login', false);
    var data = {
        'server_url': 'test', 
        'password': 'test', 
        'login': 'test'
    };
    request.setRequestHeader('Content-Type', 'application/json');
    // request.send(JSON.stringify(data));
    // if (request.status === 200) {
        // console.log(request.responseText);
    // }

    function reqListener () {
        console.log(this.responseText);
    }
    
    // TODO - синхронный запрос не работает, а асинхронный работает
    // TODO - где раположить view и presenter - main or renderer process electron
    // TODO - как организовать работу запросов к сервису?
    var oReq = new XMLHttpRequest();
    oReq.onload = reqListener;
    oReq.open('get', 'http://127.0.0.1:5000/', true);
    oReq.setRequestHeader('Content-Type', 'application/json');
    oReq.send(JSON.stringify(data));
});