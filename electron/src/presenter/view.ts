import { IView, IPresenter } from './contract';
import { BuildProperties, BuildVillageInfo, VillageInfo, Point, LoginData } from '../data/dataTypes';
import { Presenter } from './presenter';
import { RendererProcessActionTypes, MainProcessActionTypes } from './../process/ActionTypes'
import { app, BrowserWindow } from "electron";
import * as path from "path";

export class View implements IView {
    private presenter: IPresenter;
    private mainWindow: Electron.BrowserWindow;
    private ipc: Electron.IpcMain;

    constructor() {
        this.createWindow()
        this.presenter = new Presenter(this)
        this.presenter.init()
    }

    showLoginWindow(): void {
        this.mainWindow.loadFile(path.join(__dirname, "../../electron/resources/login.html"));
    }
    showVillagePropertiesWindow(defaultProperties: BuildProperties): void {
        this.mainWindow.loadFile(path.join(__dirname, "../../electron/resources/villageprop.html"));
        this.ipc.on(RendererProcessActionTypes.LOAD_VILLAGE_PARAMS_PAGE, function(event: any) {
            event.sender.send(
                MainProcessActionTypes.VILLAGE_PARAMS_DATA, 
                JSON.stringify(defaultProperties)
            );
        });
    }
    showBotWorkingWindow(): void {
        // other
        this.mainWindow.loadFile(path.join(__dirname, "../../electron/resources/login.html"));
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

        this.ipc = require('electron').ipcMain;
        this.ipc.on(RendererProcessActionTypes.LOGIN, function(event: any, response: any) {
            var loginData: LoginData = JSON.parse(response);
            main_view.presenter.login(loginData);
        });
        this.ipc.on(RendererProcessActionTypes.START_WORK, function(event: any, response: any) {
            var buildProperties: BuildProperties = JSON.parse(response);
            main_view.presenter.startWork(buildProperties);
        });
    }
}