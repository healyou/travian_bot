import { LoginData } from '../data/dataTypes'
import { XMLHttpRequest } from 'xmlhttprequest-ts';

export interface BotService {
    login(loginData: LoginData): boolean;
    quit(): void;
}

export class BotServiceImpl implements BotService {
    login(loginData: LoginData): boolean {
        var request = new XMLHttpRequest();
        request.open('post', 'http://127.0.0.1:5000/login', true);
        var data = {
            'server_url': loginData.serverUrl, 
            'password': loginData.psw, 
            'login': loginData.login
        };
        request.setRequestHeader('Content-Type', 'application/json');
        function reqListener () {
            console.log(this.responseText);
        }
        request.onload = reqListener;
        request.send(JSON.stringify(data));
        if (request.status === 200) {
            console.log(request.responseText);
        }

        return true
    }    
    quit(): void {
        // TODO nothing
    }
}