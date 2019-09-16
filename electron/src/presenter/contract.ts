import { BuildProperties } from './properties';

export interface IView {
    showLoginWindow(): void;
    showVillagePropertiesWindow(defaultProperties: BuildProperties): void;
    showBotWorkingWindow(): void;
    disableWindow(): void;
    enableWindow(): void;
    quit(): void;
}

export interface IPresenter {
    init(): void;
    login(serverUrl: string, login: string, psw: string): void;
    startWork(defaultProperties: BuildProperties): void;
    stopWork(): void;
    quit(): void;
}