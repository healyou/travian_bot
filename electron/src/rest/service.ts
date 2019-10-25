import { LoginData, BuildProperties } from '../data/dataTypes'
import { SyncJsonRequest } from './request';
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
        var request = new SyncJsonRequest('post', 'http://127.0.0.1:5000/login', JSON.stringify(data));
        return request.send();
    }
    public getVillagesInfo(): Promise<BuildProperties> {
        var request = new SyncJsonRequest('get', 'http://127.0.0.1:5000/villages_info');
        return request.send().then(function (jsonData: string): Promise<BuildProperties> {
            return new Promise<BuildProperties>(function (resolve, reject) {
                try {
                    var propJson = JSON.stringify(JSON.parse(jsonData).answer);
                    var buildProperties = DeserializeUtils.buildPropertiesFromJson(propJson);
                    resolve(buildProperties);
                } catch(error) {
                    reject(error);
                }
            });
        });
    }
    public startWork(defaultProperties: BuildProperties): Promise<string> {
        var request = new SyncJsonRequest('post', 'http://127.0.0.1:5000/startWork', JSON.stringify(defaultProperties));
        return request.send();
    }
    public stopWork(): Promise<string> {
        var request = new SyncJsonRequest('get', 'http://127.0.0.1:5000/stopWork');
        return request.send();
    }
}