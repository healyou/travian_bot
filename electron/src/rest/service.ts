import { LoginData, BuildProperties, BuildVillageInfo, VillageInfo, Point } from '../data/dataTypes'
import { XMLHttpRequest } from 'xmlhttprequest-ts';
import { SyncJsonRequest } from './request';

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
                    let prop = Object.create(BuildProperties.prototype);
                    resolve(BotServiceImpl.decodeBuildProperties(jsonData));
                } catch(error) {
                    reject(error);
                }
            });
        });
    }
    // TODO - написать конвертер из json в объекты со свойствами name_x to nameX
    private static decodeBuildProperties(json: string): BuildProperties {
        return {
            infoList: this.decodeInfoList(json)
        };
    }
    private static decodeInfoList(json: string): Array<BuildVillageInfo> {
        var infos: Array<BuildVillageInfo> = new Array();
        JSON.parse(json).answer.info_list.forEach((item: Object) => {
            infos.push(this.decodeBuildVillageInfo(item))
        });
        return infos;
    }
    private static decodeBuildVillageInfo(object: any): BuildVillageInfo {
        return {
            info: new VillageInfo(object.info.name, this.decodePoint(object.info.point)),
            autoBuildRes: object.auto_build_res
        }
    } 
    private static decodePoint(object: any): Point {
        return {
            x: object.x,
            y: object.y
        }
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