// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.
import { RendererProcessActionTypes, MainProcessActionTypes } from '../process/ActionTypes'
import { BuildProperties, BuildVillageInfo, Point } from '../data/dataTypes';

var ipc = require('electron').ipcRenderer;
var savedBuildProps: BuildProperties = null;

var saveButton = document.getElementById('saveVillagesParams');
saveButton.addEventListener('click', function(){
    saveButton.setAttribute('disabled', 'true');
    ipc.send(RendererProcessActionTypes.START_WORK, JSON.stringify(savedBuildProps));
});

ipc.once(MainProcessActionTypes.VILLAGE_PARAMS_DATA, function(event: any, response: any){
    console.log(response);
    var buildProps: BuildProperties = JSON.parse(response);
    var villageInfoElem = document.getElementById('villageInfo');
    savedBuildProps = buildProps;

    var propHtml = "";
    var i = 0;

    buildProps.infoList.forEach(function (villageInfo: BuildVillageInfo) {
        var autoBuildResource: boolean = villageInfo.autoBuildRes;
        var villageCoord: Point = villageInfo.info.point;
        var villageName: String = villageInfo.info.name;

        var coordText: String = `${villageCoord.x}/${villageCoord.y}`;
        var checkedValue: String = autoBuildResource ? "checked" : "";
        
        propHtml += `
        <li class="list-group-item">
            ${villageName} - <span class="badge badge-secondary">${coordText}</span>
            <div class="form-check float-right">
                <input type="checkbox" class="form-check-input" ${checkedValue} id="autoBuildRes${i++}">
                <label class="form-check-label" for="exampleCheck1">Автоматическое строительство ресурсов</label>
            </div>
        </li>
        `;
    });

    villageInfoElem.innerHTML = propHtml;
});
ipc.send(RendererProcessActionTypes.LOAD_VILLAGE_PARAMS_PAGE);