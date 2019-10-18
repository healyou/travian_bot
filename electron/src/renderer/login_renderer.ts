// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.
import { XMLHttpRequest } from 'xmlhttprequest-ts';
import { RendererProcessActionTypes } from '../process/ActionTypes'


function processResponse(response: any) {
    console.log(response);
}

var ipc = require('electron').ipcRenderer;

var authButton = document.getElementById('login');
var emailInput = <HTMLInputElement>document.getElementById('email');
var passwordInput = <HTMLInputElement>document.getElementById('password');
var messageElement = <HTMLElement>document.getElementById('message');

function validateFormData(email: String, password: String): Boolean {
    if (!email.trim() || !password.trim()) {
        messageElement.innerHTML = "Необходимо ввести данные";
        return false;
    } else {
        return true;
    }
}

authButton.addEventListener('click', function(){
    ipc.once('actionReply', function(event: any, response: any){
        processResponse(response);
    });

    var email = emailInput.value;
    var password = passwordInput.value;

    if (validateFormData(email, password)) {
        var formData = {
            email: email,
            password: password
        };
    
        ipc.send(RendererProcessActionTypes.LOGIN, JSON.stringify(formData));
    }
    // TODO - синхронный запрос не работает, а асинхронный работает
    // TODO - где раположить view и presenter - main or renderer process electron
    // TODO - как организовать работу запросов к сервису?
});