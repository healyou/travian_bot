import { XMLHttpRequest } from 'xmlhttprequest-ts';

export class JsonRequest {
    private method: string;
    private url: string;
    private jsonData: string;

    constructor(method: string, url: string, jsonData: string = "") {
        this.method = method;
        this.url = url;
        this.jsonData = jsonData;
    }

    public send(): Promise<string> {
        var jsonRequest = this;
        return new Promise<string>(function (resolve, reject) {
            var xhr = new XMLHttpRequest();
            xhr.open(jsonRequest.method, jsonRequest.url, true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.timeout = 30000;
            xhr.ontimeout = function (err: Error) {
                reject({
                    status: this.status,
                    statusText: xhr.statusText
                });
            };
            xhr.onload = function () {
                if (this.status >= 200 && this.status < 300) {
                    resolve(xhr.responseText);
                } else {
                    reject({
                        status: this.status,
                        statusText: xhr.statusText
                    });
                }
            };
            xhr.onerror = function () {
                reject({
                    status: this.status,
                    statusText: xhr.statusText
                });
            };
            xhr.send(jsonRequest.jsonData);
        });
    }
}