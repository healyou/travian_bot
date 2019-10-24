import { IView, IPresenter } from './contract';
import { BuildProperties, LoginData, BuildVillageInfo, VillageInfo, Point } from '../data/dataTypes';
import * as path from "path";
import { XMLHttpRequest } from 'xmlhttprequest-ts';
import { BotServiceImpl, BotService } from '../rest/service'
import { resolve } from 'url';

export class Presenter implements IPresenter {
    private view: IView;
    private botService: BotService;

    constructor(view: IView) {
        this.view = view;
        this.botService = new BotServiceImpl();
    }

    init(): void {
        this.runPython();
        this.view.showLoginWindow();
    }
    login(loginData: LoginData): void {
        var presenter = this;
        this.botService.login(loginData).then(function (value: string) {
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
            presenter.botService.getVillagesInfo().then(function (value: BuildProperties) {
                console.log(JSON.stringify(value));
                presenter.view.showVillagePropertiesWindow(value);
            }).catch(function (error: any) {
                var message = 'Внутренняя ошибка1: ' + JSON.stringify(error);
                presenter.view.showError(message);
            });
        }).catch(function (error: any) {
            var message = 'Внутренняя ошибка: ' + JSON.stringify(error);
            presenter.view.showError(message);
        });
    }
    startWork(defaultProperties: BuildProperties): void {
        var presenter = this;
        this.botService.startWork(defaultProperties).then(function (value: string) {
            presenter.view.showBotWorkingWindow();
        }).catch(function (error: any) {
            console.log(JSON.stringify(error));
        });
    }
    stopWork(): void {
        var presenter = this;
        this.closeBotWork().then(function (value: string) {
            presenter.view.showLoginWindow();
        }).catch(function (error: any) {
            console.log(JSON.stringify(error));
        });
    }
    quit(): void {
        this.closeBotWork().then(function (value: string) {

        }).catch(function (error: any) {
            console.log(JSON.stringify(error));
        });
    }

    private closeBotWork(): Promise<string> {
        return this.botService.stopWork()
    }

    private runPython(): void {
        // create console
        var nodeConsole = require('console');
        var myConsole = new nodeConsole.Console(process.stdout, process.stderr);
        myConsole.log(__dirname);

        // run python flask server
        var pythonPath = path.join(__dirname, '../../.venv/Scripts/python')
        var scriptPath = path.join(__dirname, '../../mainflask.py')
        var python = require('child_process').spawn(pythonPath, [scriptPath]);
        python.stdout.on('data', (data: any) => {
            console.log("data: ",data.toString('utf8'));
        });
        python.stderr.on('close', () => {
            console.log("Closed");
        });
    }
}