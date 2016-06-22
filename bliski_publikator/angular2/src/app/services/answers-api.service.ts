import { Injectable } from '@angular/core';
import { Http } from '@angular/http';

import { BaseApiService } from './api.base.service';

import { CsrfService } from '../services/csrf.service';

@Injectable()
export class AnswerService extends BaseApiService {

    constructor(http: Http, csrf: CsrfService) {
        super(http, csrf);
    }

    saveAnswers(answers: { id: number, value: string, point: number }[]) {
        let result = answers;
        let point = answers.reduce((prev, curr) => prev + curr.point, 0);
        return this.simple_post(document.location.href, {result, point});
    }
}
