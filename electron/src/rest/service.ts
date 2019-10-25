import { LoginData, BuildProperties } from '../data/dataTypes'
import { JsonRequest } from './request';
import { DeserializeUtils } from '../data/deserialize';

export interface BotService {
    login(loginData: LoginData): Promise<string>;
    getVillagesInfo(): Promise<BuildProperties>;
    startWork(defaultProperties: BuildProperties): Promise<string>;
    stopWork(): Promise<string>;
}

export class BotServiceImpl implements BotService {
    public login(loginData: LoginData): Promise<string> {
        var data = {
            'server_url': loginData.serverUrl, 
            'password': loginData.psw, 
            'login': loginData.login
        };
        var request = new JsonRequest('post', 'http://127.0.0.1:5000/login', JSON.stringify(data));
        return request.send().then(function (requestData) {
            return new Promise<string>(function (resolve, reject) {
                BotServiceImpl.analizeAnswer(requestData, resolve, reject);
            });
        });
    }
    public getVillagesInfo(): Promise<BuildProperties> {
        var request = new JsonRequest('get', 'http://127.0.0.1:5000/villages_info');
        return request.send().then(function (requestData: string): Promise<BuildProperties> {
            return new Promise<BuildProperties>(function (resolve, reject) {
                BotServiceImpl.analizeRequestAnswer(requestData, reject, function(jsonAnswer: string) {
                    try {
                        var propJson = JSON.stringify(JSON.parse(jsonAnswer).answer);
                        var buildProperties = DeserializeUtils.buildPropertiesFromJson(propJson);
                        resolve(buildProperties);
                    } catch(error) {
                        reject(error);
                    }
                })
            });
        });
    }
    public startWork(defaultProperties: BuildProperties): Promise<string> {
        var request = new JsonRequest('post', 'http://127.0.0.1:5000/startWork', JSON.stringify(defaultProperties));
        return request.send().then(function (requestData) {
            return new Promise<string>(function (resolve, reject) {
                BotServiceImpl.analizeAnswer(requestData, resolve, reject);
            });
        });
    }
    public stopWork(): Promise<string> {
        var request = new JsonRequest('get', 'http://127.0.0.1:5000/stopWork');
        return request.send().then(function (requestData) {
            return new Promise<string>(function (resolve, reject) {
                BotServiceImpl.analizeAnswer(requestData, resolve, reject);
            });
        });
    }

    private static analizeAnswer(
        jsonAnswer: string,
        resolve: (value?: string) => void,
        reject: (reason?: any) => void,
    ) {
        BotServiceImpl.analizeRequestAnswer(jsonAnswer, reject, resolve);
    } 

    private static analizeRequestAnswer(
        jsonAnswer: string,  
        reject: (reason?: any) => void,
        callback: (jsonAnswer: string) => void
    ) {
        var answerObject = JSON.parse(jsonAnswer);
        var result = answerObject.result
        if (result) {
            callback(jsonAnswer);
        } else {
            var error = answerObject.error;
            reject(error);
        }
    }
}