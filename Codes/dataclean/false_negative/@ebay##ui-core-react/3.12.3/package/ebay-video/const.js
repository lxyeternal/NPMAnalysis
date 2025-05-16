"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.defaultVideoConfig = exports.ERROR_NO_PLAYER = exports.ERROR_ANOTHER_LOAD = void 0;
exports.ERROR_ANOTHER_LOAD = 7000;
exports.ERROR_NO_PLAYER = 11;
exports.defaultVideoConfig = {
    addBigPlayButton: false,
    addSeekBar: true,
    controlPanelElements: [
        'play_pause',
        'time_and_duration',
        'spacer',
        'mute',
        'report',
        'captions',
        // 'quality', // uncomment this to show a gear icon for video quality control
        'fullscreen'
    ]
};
