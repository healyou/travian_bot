import { IView, IPresenter } from './contract';
import { BuildProperties, LoginData, BuildVillageInfo, VillageInfo, Point } from '../data/dataTypes';
import * as path from "path";
import { XMLHttpRequest } from 'xmlhttprequest-ts';

export class Presenter implements IPresenter {
    private view: IView;

    constructor(view: IView) {
        this.view = view;
    }

    init(): void {
        // this.runPython();
        this.view.showLoginWindow();
    }
    login(loginData: LoginData): void {
        var request = new XMLHttpRequest();
        request.open('post', 'http://127.0.0.1:5000/login', false);
        request.setRequestHeader('Content-Type', 'application/json');
        // request.send(JSON.stringify(loginData));
        // if (request.status === 200) {
        //     console.log(request.responseText);
        // }

        var villagesInfo = new Array<BuildVillageInfo>(
            new BuildVillageInfo(
                new VillageInfo("village1", new Point(50, 50)),
                false
            ),
            new BuildVillageInfo(
                new VillageInfo("village2", new Point(150, 150)),
                false
            ),
            new BuildVillageInfo(
                new VillageInfo("village3", new Point(70, 150)),
                true
            )
        );
        var prop: BuildProperties = new BuildProperties(villagesInfo);
        this.view.showVillagePropertiesWindow(prop);
    }
    startWork(defaultProperties: BuildProperties): void {
        this.view.showBotWorkingWindow();
    }
    stopWork(): void {
        var request = new XMLHttpRequest();
        request.open('get', 'http://127.0.0.1:5000/stopWork', false);
        request.setRequestHeader('Content-Type', 'application/json');
        request.send(null);
        if (request.status === 200) {
            console.log(request.responseText);
        }
    }
    quit(): void {
        this.stopWork();
    }

    private runPython(): void {
        // create console
        var nodeConsole = require('console');
        var myConsole = new nodeConsole.Console(process.stdout, process.stderr);
        myConsole.log(__dirname);

        // run python flask server
        var pythonPath = path.join(__dirname, '../../.venv/Scripts/python')
        var scriptPath = path.join(__dirname, '../../maingui.py')
        var python = require('child_process').spawn(pythonPath, [scriptPath]);
        python.stdout.on('data', (data: any) => {
            console.log("data: ",data.toString('utf8'));
        });
        python.stderr.on('close', () => {
            console.log("Closed");
        });
    }
}