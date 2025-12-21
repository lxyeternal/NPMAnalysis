import * as i0 from '@angular/core';
import { Injectable, Component, NgModule } from '@angular/core';
import * as i1 from '@angular/common/http';
import { HttpHeaders, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

class TestService {
    constructor() { }
    static { this.ɵfac = i0.ɵɵngDeclareFactory({ minVersion: "12.0.0", version: "16.1.4", ngImport: i0, type: TestService, deps: [], target: i0.ɵɵFactoryTarget.Injectable }); }
    static { this.ɵprov = i0.ɵɵngDeclareInjectable({ minVersion: "12.0.0", version: "16.1.4", ngImport: i0, type: TestService, providedIn: 'root' }); }
}
i0.ɵɵngDeclareClassMetadata({ minVersion: "12.0.0", version: "16.1.4", ngImport: i0, type: TestService, decorators: [{
            type: Injectable,
            args: [{
                    providedIn: 'root'
                }]
        }], ctorParameters: function () { return []; } });

class ApiConfigService {
    static { this.ɵfac = i0.ɵɵngDeclareFactory({ minVersion: "12.0.0", version: "16.1.4", ngImport: i0, type: ApiConfigService, deps: [], target: i0.ɵɵFactoryTarget.Injectable }); }
    static { this.ɵprov = i0.ɵɵngDeclareInjectable({ minVersion: "12.0.0", version: "16.1.4", ngImport: i0, type: ApiConfigService, providedIn: 'root' }); }
}
i0.ɵɵngDeclareClassMetadata({ minVersion: "12.0.0", version: "16.1.4", ngImport: i0, type: ApiConfigService, decorators: [{
            type: Injectable,
            args: [{
                    providedIn: 'root',
                }]
        }] });

// import { Component, ElementRef } from '@angular/core';
// import { HttpClient, HttpHeaders } from '@angular/common/http';
// interface ApiResponse {
//   pipelineResponse?: {
//     audio?: {
//       audioContent?: string;
//     }[];
//   }[];
// }
// @Component({
//   selector: 'lib-test',
//   template: `
//     <p>
//       test works!
//     </p>
//   `,
//   styles: [
//   ]
// })
// export class TestComponent {
//     audioElement: HTMLAudioElement = new Audio();
//   ttsOutput: string | undefined;
//   constructor(private http: HttpClient, private elementRef: ElementRef) {}
//   convertToSpeech() {
//     const url = 'https://dhruva-api.bhashini.gov.in/services/inference/pipeline';
//     const userId = '26f83e9d425a40a28ec59f944cb4da6c';
//     const apiKey = '1829da2d40-6a44-4d3d-ac61-9850afd41175';
//     const authorizationToken = 'cYZieH0OCn8PUZbylALnCkwvs8PYvAiYwiQ7FUj1V7_Vspia5jvxFs0T3R3-DXF_';
//     const headers = new HttpHeaders({
//       'Content-Type': 'application/json',
//       'userID': userId,
//       'ulcaApiKey': apiKey,
//       'Authorization': authorizationToken
//     });
//     const text = this.elementRef.nativeElement.querySelector('#textElement').innerText.trim();
//     const payload = {
//       pipelineTasks: [
//         {
//           taskType: 'tts',
//           config: {
//             language: {
//               sourceLanguage: 'en'
//             },
//             serviceId: 'ai4bharat/indic-tts-coqui-misc-gpu--t4',
//             gender: 'female',
//             samplingRate: 8000
//           }
//         }
//       ],
//       inputData: {
//         input: [
//           {
//             source: text
//           }
//         ]
//       }
//     };
//     this.http.post<ApiResponse>(url, payload, { headers }).subscribe(
//       response => {
//         console.log('API response:', response);
//         if (
//           response.pipelineResponse &&
//           response.pipelineResponse.length > 0 &&
//           response.pipelineResponse[0].audio &&
//           response.pipelineResponse[0].audio.length > 0 &&
//           response.pipelineResponse[0].audio[0].audioContent
//         ) {
//           this.ttsOutput = response.pipelineResponse[0].audio[0].audioContent;
//           this.playAudio();
//         } else {
//           this.ttsOutput = undefined;
//         }
//       },
//       error => {
//         console.error('API error:', error);
//         // Handle the error here
//       }
//     );
//   }
//   playAudio() {
//     if (this.ttsOutput) {
//       const audioUrl = `data:audio/wav;base64,${this.ttsOutput}`;
//       this.audioElement.src = audioUrl;
//       this.audioElement.load();
//       this.audioElement.play();
//     }
//   }
// }
class TestComponent {
    constructor(http, elementRef, apiConfig) {
        this.http = http;
        this.elementRef = elementRef;
        this.apiConfig = apiConfig;
        this.audioElement = new Audio();
    }
    convertToSpeech() {
        const url = 'https://dhruva-api.bhashini.gov.in/services/inference/pipeline';
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            ...(this.apiConfig.userId && { 'userID': this.apiConfig.userId }),
            ...(this.apiConfig.apiKey && { 'ulcaApiKey': this.apiConfig.apiKey }),
            ...(this.apiConfig.authorizationToken && { 'Authorization': this.apiConfig.authorizationToken }),
        });
        const text = this.elementRef.nativeElement.querySelector('#textElement').innerText.trim();
        const payload = {
            pipelineTasks: [
                {
                    taskType: 'tts',
                    config: {
                        language: {
                            sourceLanguage: 'en'
                        },
                        serviceId: 'ai4bharat/indic-tts-coqui-misc-gpu--t4',
                        gender: 'female',
                        samplingRate: 8000
                    }
                }
            ],
            inputData: {
                input: [
                    {
                        source: text
                    }
                ]
            }
        };
        this.http.post(url, payload, { headers }).subscribe(response => {
            console.log('API response:', response);
            if (response.pipelineResponse &&
                response.pipelineResponse.length > 0 &&
                response.pipelineResponse[0].audio &&
                response.pipelineResponse[0].audio.length > 0 &&
                response.pipelineResponse[0].audio[0].audioContent) {
                this.ttsOutput = response.pipelineResponse[0].audio[0].audioContent;
                this.playAudio();
            }
            else {
                this.ttsOutput = undefined;
            }
        }, error => {
            console.error('API error:', error);
            // Handle the error here
        });
    }
    playAudio() {
        if (this.ttsOutput) {
            const audioUrl = `data:audio/wav;base64,${this.ttsOutput}`;
            this.audioElement.src = audioUrl;
            this.audioElement.load();
            this.audioElement.play();
        }
    }
    static { this.ɵfac = i0.ɵɵngDeclareFactory({ minVersion: "12.0.0", version: "16.1.4", ngImport: i0, type: TestComponent, deps: [{ token: i1.HttpClient }, { token: i0.ElementRef }, { token: ApiConfigService }], target: i0.ɵɵFactoryTarget.Component }); }
    static { this.ɵcmp = i0.ɵɵngDeclareComponent({ minVersion: "14.0.0", version: "16.1.4", type: TestComponent, selector: "lib-test", ngImport: i0, template: "<div id=\"textElement\">\r\n    The real meaning of development is the process of improving the quality of all human lives and capabilities by raising people\u2019s levels of living, self-esteem, and freedom. Development is a multidimensional process that involving changes in the social structures, the popular attitudes and national institutions, and the acceleration of economic growth.   \r\n  </div>\r\n  \r\n  <button (click)=\"convertToSpeech()\">Speech</button>" }); }
}
i0.ɵɵngDeclareClassMetadata({ minVersion: "12.0.0", version: "16.1.4", ngImport: i0, type: TestComponent, decorators: [{
            type: Component,
            args: [{ selector: 'lib-test', template: "<div id=\"textElement\">\r\n    The real meaning of development is the process of improving the quality of all human lives and capabilities by raising people\u2019s levels of living, self-esteem, and freedom. Development is a multidimensional process that involving changes in the social structures, the popular attitudes and national institutions, and the acceleration of economic growth.   \r\n  </div>\r\n  \r\n  <button (click)=\"convertToSpeech()\">Speech</button>" }]
        }], ctorParameters: function () { return [{ type: i1.HttpClient }, { type: i0.ElementRef }, { type: ApiConfigService }]; } });

class TestModule {
    static { this.ɵfac = i0.ɵɵngDeclareFactory({ minVersion: "12.0.0", version: "16.1.4", ngImport: i0, type: TestModule, deps: [], target: i0.ɵɵFactoryTarget.NgModule }); }
    static { this.ɵmod = i0.ɵɵngDeclareNgModule({ minVersion: "14.0.0", version: "16.1.4", ngImport: i0, type: TestModule, declarations: [TestComponent], imports: [CommonModule,
            HttpClientModule,
            FormsModule], exports: [TestComponent] }); }
    static { this.ɵinj = i0.ɵɵngDeclareInjector({ minVersion: "12.0.0", version: "16.1.4", ngImport: i0, type: TestModule, providers: [ApiConfigService], imports: [CommonModule,
            HttpClientModule,
            FormsModule] }); }
}
i0.ɵɵngDeclareClassMetadata({ minVersion: "12.0.0", version: "16.1.4", ngImport: i0, type: TestModule, decorators: [{
            type: NgModule,
            args: [{
                    declarations: [
                        TestComponent
                    ],
                    imports: [
                        CommonModule,
                        HttpClientModule,
                        FormsModule,
                    ],
                    providers: [ApiConfigService],
                    exports: [
                        TestComponent
                    ]
                }]
        }] });

/*
 * Public API Surface of test
 */

/**
 * Generated bundle index. Do not edit.
 */

export { ApiConfigService, TestComponent, TestModule, TestService };
//# sourceMappingURL=test.mjs.map
