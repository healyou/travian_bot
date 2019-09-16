import { IView, IPresenter } from './contract';
import { BuildProperties } from './properties';
import { Presenter } from './presenter';
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
        this.presenter.login('', '', '');
    }

    showLoginWindow(): void {
        // and load the index.html of the app.
        this.mainWindow.loadFile(path.join(__dirname, "../../electron/resources/index.html"));
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

        var ipc = require('electron').ipcMain;
        ipc.on('invokeAction', function(event: any, data: any) {
            console.log('data from renderer process - ' + data);
            var result = 'data from main process';
            // main_view.onLoginClick();
            event.sender.send('actionReply', result);
        });
    }
}