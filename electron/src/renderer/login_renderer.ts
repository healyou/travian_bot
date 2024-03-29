// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.
import { LoginData } from '../data/dataTypes';
import { RendererProcessActionTypes, MainProcessActionTypes } from '../process/ActionTypes'


var ipc = require('electron').ipcRenderer;

var authButton = document.getElementById('login');
var serverUrlInput = <HTMLInputElement>document.getElementById('serverUrl');
var emailInput = <HTMLInputElement>document.getElementById('email');
var passwordInput = <HTMLInputElement>document.getElementById('password');
var messageElement = <HTMLElement>document.getElementById('message');

function validateFormData(loginData: LoginData): Boolean {
    if (!loginData.login.trim() || !loginData.psw.trim() || !loginData.serverUrl.trim()) {
        messageElement.innerHTML = "Необходимо ввести данные";
        return false;
    } else {
        return true;
    }
}

authButton.addEventListener('click', function(){
    var email = emailInput.value;
    var password = passwordInput.value;
    var serverUrl = serverUrlInput.value;
    var loginData: LoginData = new LoginData(serverUrl, email, password);

    if (validateFormData(loginData)) {
        authButton.setAttribute('disabled', 'true');
        ipc.send(RendererProcessActionTypes.LOGIN, JSON.stringify(loginData));
    }
});

ipc.once(MainProcessActionTypes.EXECUTION_ERROR, function(event: any, response: any) {
    authButton.setAttribute('disabled', 'false');
    messageElement.innerHTML = response;
});