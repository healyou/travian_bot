// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.
import { RendererProcessActionTypes } from '../process/ActionTypes'

var ipc = require('electron').ipcRenderer;

var closeWorkButton = document.getElementById('closeBotWork');
closeWorkButton.addEventListener('click', function(){
    ipc.send(RendererProcessActionTypes.STOP_WORK);
});