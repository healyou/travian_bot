import { BuildProperties, LoginData } from '../data/dataTypes';

export interface IView {
    showError(error: string): void;
    showLoginWindow(): void;
    showVillagePropertiesWindow(defaultProperties: BuildProperties): void;
    showBotWorkingWindow(): void;
    disableWindow(): void;
    enableWindow(): void;
    quit(): void;
}

export interface IPresenter {
    init(): void;
    login(loginData: LoginData): void;
    startWork(defaultProperties: BuildProperties): void;
    stopWork(): void;
    quit(): void;
}