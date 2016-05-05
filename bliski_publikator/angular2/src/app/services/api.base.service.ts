import { Injectable } from 'angular2/core';
import {
    Http,
    Response,
    Headers,
    RequestOptions
} from 'angular2/http';

import {CsrfService} from '../services/csrf.service';

import { Observable }     from 'rxjs/Observable';

@Injectable()
export abstract class BaseApiService {
    private _apiUrl = '/api/';
    constructor(protected _http: Http, protected _csrf: CsrfService) { }

    protected simple_post(url:string, data){
        let body = JSON.stringify(data);
        let options = this.getDefaultOptions();
        return this._http.post(url, body, options)
            .map(this.extractData)
            .catch(this.handleError);
    }

    protected simple_get(url:string, qs = {}){
        let options = this.getDefaultOptions();
        return this._http.get(url, options)
            .map(this.extractData)
            .catch(this.handleError)
    }

    private extractData(res: Response) {
        if (res.status < 200 || res.status >= 300) {
            throw new Error('Bad response status: ' + res.status);
        }
        let body = res.json();
        return body || {};
    }

    protected handleError(error: any) {
        let errMsg = error.message || 'Server error';
        console.error(errMsg);
        return Observable.throw(errMsg);
    }

    private getDefaultOptions() {
        let headers = new Headers(
            {
                'Content-Type': 'application/json',
                'X-CSRFToken': this._csrf.getToken()
            });
        return new RequestOptions({ headers: headers });
    }
}
