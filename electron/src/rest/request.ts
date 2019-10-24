import { XMLHttpRequest } from 'xmlhttprequest-ts';

export class SyncJsonRequest {
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
        // var wait: boolean = true;
        // var result: string = null;
        // var error: Error = null;

        // this.execute(
        //     function (jsonData?: string) {
        //         result = jsonData;
        //         wait = false;
        //         console.log(result);
        //     }, 
        //     function (error?: any) {
        //         wait = false;
        //         console.log(error);
        //     }
        // )

        // return "test";

        // while (wait) {
        //     var sleep = require('thread-sleep');
 
        //     var start = Date.now();
        //     var res = sleep(300);
        //     var end = Date.now();
        //     // res is the actual time that we slept for
        //     console.log(res + ' ~= ' + (end - start) + ' ~= 1000');
            // итак - в js нет асинхронности и многопоточности, поэтому asynс await и promise в помощь, иначе никак не подождать поток
            // ПОЭТОМУ НАДО ПОДУМАТЬ, КАК РЕАЛИЗОВАТЬ ТЕПЕРЬ ЧЕРЕЗ promise
            // function sleep(millis) {
            //     return new Promise(resolve => setTimeout(resolve, millis));
            // }
            // Нет зависимостей, нет ада обратного вызова; это :-)
            // Учитывая пример, приведенный в вопросе, вот как мы будем спать между двумя журналами консоли:
            // async function main() {
            //     console.log("Foo");
            //     await sleep(2000);
            //     console.log("Bar");
            // }
            
            // main();
        // }

        // if (error != null) {
        //     throw error;
        // } else {
        //     return result;
        // }
    }

    private execute(resolve: (value?: string) => void, reject: (reason?: any) => void): void {
        var xhr = new XMLHttpRequest();
        xhr.open(this.method, this.url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.timeout = 10000;
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
        xhr.send(this.jsonData);
    }
}