import { IView, IPresenter } from './contract';
import { BuildProperties } from './properties';
import * as path from "path";
import { XMLHttpRequest } from 'xmlhttprequest-ts';

export class Presenter implements IPresenter {
    private view: IView;

    constructor(view: IView) {
        this.view = view;
    }

    init(): void {
        this.runPython();
        this.view.showLoginWindow();
    }
    login(serverUrl: string, login: string, psw: string): void {
        var request = new XMLHttpRequest();
        request.open('post', 'http://127.0.0.1:5000/login', false);
        var data = {
            'server_url': 'test', 
            'password': 'test', 
            'login': 'test'
        };
        request.setRequestHeader('Content-Type', 'application/json');
        request.send(JSON.stringify(data));
        if (request.status === 200) {
            console.log(request.responseText);
        }
    }
    startWork(defaultProperties: BuildProperties): void {
        throw new Error("Method not implemented.");
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