import { IView, IPresenter } from './contract';
import { BuildProperties, BuildVillageInfo, VillageInfo, Point } from '../data/dataTypes';
import { Presenter } from './presenter';
import { RendererProcessActionTypes, MainProcessActionTypes } from './../process/ActionTypes'
import { app, BrowserWindow } from "electron";
import * as path from "path";

export class View implements IView {
    private presenter: IPresenter
    private mainWindow: Electron.BrowserWindow

    constructor() {
        this.createWindow()
        this.presenter = new Presenter(this)
        this.presenter.init()
    }

    public onLoginClick() {
        this.mainWindow.loadFile(path.join(__dirname, "../../electron/resources/villageprop.html"));
        // this.presenter.login('', '', '');
    }

    showLoginWindow(): void {
        // and load the index.html of the app.
        this.mainWindow.loadFile(path.join(__dirname, "../../electron/resources/login.html"));
    }
    showVillagePropertiesWindow(defaultProperties: BuildProperties): void {
        throw new Error("Method not implemented.");
    }
    showBotWorkingWindow(): void {
        throw new Error("Method not implemented.");
    }
    disableWindow(): void {
        throw new Error("Method not implemented.");
    }
    enableWindow(): void {
        throw new Error("Method not implemented.");
    }
    quit(): void {
        this.mainWindow.close();
        this.mainWindow.destroy();
        this.presenter.quit();
    }

    private createWindow(): void {
        // Create the browser window.
        this.mainWindow = new BrowserWindow({
            height: 600,
            width: 800,
        });

        // Open the DevTools.
        this.mainWindow.webContents.openDevTools();

        // Emitted when the window is closed.
        this.mainWindow.on("closed", () => {
            // Dereference the window object, usually you would store windows
            // in an array if your app supports multi windows, this is the time
            // when you should delete the corresponding element.
            this.mainWindow = null;
        });

        var main_view = this;
        var mainWindow = this.mainWindow;

        var ipc = require('electron').ipcMain;
        var ipcRenderer = require('electron').ipcRenderer
        ipc.on(RendererProcessActionTypes.LOGIN, function(event: any, data: any) {
            ipc.on(RendererProcessActionTypes.LOAD_VILLAGE_PARAMS_PAGE, function(event: any, data: any) {
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
                event.sender.send(MainProcessActionTypes.VILLAGE_PARAMS_DATA, JSON.stringify(prop));
            });

            console.log('data from renderer process - ' + data);
            main_view.onLoginClick();
        });
        ipc.on(RendererProcessActionTypes.START_WORK, function(event: any, data: any) {
            console.log('data from renderer process - ' + data);
            var result = 'data from main process';
            mainWindow.webContents.send('actionReply', result);
        });
    }
}