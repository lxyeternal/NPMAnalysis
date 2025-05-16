"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __rest = (this && this.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
};
var __spreadArrays = (this && this.__spreadArrays) || function () {
    for (var s = 0, i = 0, il = arguments.length; i < il; i++) s += arguments[i].length;
    for (var r = Array(s), k = 0, i = 0; i < il; i++)
        for (var a = arguments[i], j = 0, jl = a.length; j < jl; j++, k++)
            r[k] = a[j];
    return r;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = __importStar(require("react"));
var classnames_1 = __importDefault(require("classnames"));
var shaka_player_ui_1 = __importDefault(require("shaka-player/dist/shaka-player.ui"));
require("shaka-player/dist/controls.css");
var component_utils_1 = require("../common/component-utils");
var index_1 = require("../index");
var source_1 = __importDefault(require("./source"));
var const_1 = require("./const");
var controls_1 = require("./controls");
var EbayVideo = function (_a) {
    var width = _a.width, height = _a.height, thumbnail = _a.thumbnail, action = _a.action, muted = _a.muted, _b = _a.playView, playView = _b === void 0 ? 'inline' : _b, a11yLoadText = _a.a11yLoadText, a11yPlayText = _a.a11yPlayText, reportText = _a.reportText, volumeSlider = _a.volumeSlider, _c = _a.volume, volume = _c === void 0 ? 1 : _c, errorText = _a.errorText, _d = _a.onVolumeChange, onVolumeChange = _d === void 0 ? function () {
    } : _d, _e = _a.onLoadError, onLoadError = _e === void 0 ? function () {
    } : _e, _f = _a.onPlay, onPlay = _f === void 0 ? function () {
    } : _f, _g = _a.onReport, onReport = _g === void 0 ? function () {
    } : _g, children = _a.children, rest = __rest(_a, ["width", "height", "thumbnail", "action", "muted", "playView", "a11yLoadText", "a11yPlayText", "reportText", "volumeSlider", "volume", "errorText", "onVolumeChange", "onLoadError", "onPlay", "onReport", "children"]);
    var _h = react_1.useState(), loaded = _h[0], setLoaded = _h[1];
    var _j = react_1.useState(), buffering = _j[0], setBuffering = _j[1];
    var _k = react_1.useState(), playing = _k[0], setPlaying = _k[1];
    var _l = react_1.useState(), failed = _l[0], setFailed = _l[1];
    var containerRef = react_1.useRef(null);
    var videoRef = react_1.useRef(null);
    var playerRef = react_1.useRef(null);
    var uiRef = react_1.useRef(null);
    var sources = component_utils_1.filterByType(children, source_1.default).map(function (_a) {
        var props = _a.props;
        return props;
    });
    var handleError = function (err) {
        setLoaded(true);
        setFailed(true);
        onLoadError(err);
    };
    var loadSource = function (index) {
        var _a;
        if (index === void 0) { index = 0; }
        if (!sources.length || !playerRef.current)
            return;
        setLoaded(false);
        playerRef.current
            .load((_a = sources[index]) === null || _a === void 0 ? void 0 : _a.src)
            .then(function () {
            setFailed(false);
        })
            .catch(function (err) {
            console.error(err);
            switch (err.code) {
                case const_1.ERROR_ANOTHER_LOAD:
                    return;
                case const_1.ERROR_NO_PLAYER:
                    setTimeout(function () { return loadSource(index); }, 0);
                    break;
                default: {
                    var nextIndex_1 = sources.length > index + 1 && index + 1;
                    if (nextIndex_1) {
                        setTimeout(function () { return loadSource(nextIndex_1); }, 0);
                    }
                    else {
                        handleError(err);
                    }
                }
            }
        })
            .finally(function () {
            setLoaded(true);
        });
    };
    react_1.useEffect(function () {
        var video = videoRef.current;
        var container = containerRef.current;
        if (!video || !container)
            return;
        video.volume = volume;
        shaka_player_ui_1.default.polyfill.installAll(); // todo: check if we need that
        playerRef.current = new shaka_player_ui_1.default.Player(video);
        if (!playerRef.current)
            return;
        playerRef.current.addEventListener('error', handleError);
        playerRef.current.addEventListener('buffering', function (e) {
            setBuffering(e.buffering);
        });
        uiRef.current = new shaka_player_ui_1.default.ui.Overlay(playerRef.current, container, video, reportText);
        uiRef.current.configure({
            addBigPlayButton: true,
            controlPanelElements: [],
            addSeekBar: false
        });
        var _a = controls_1.customControls(onReport), Report = _a.Report, TextSelection = _a.TextSelection;
        shaka_player_ui_1.default.ui.Controls.registerElement('report', new Report.Factory(reportText));
        shaka_player_ui_1.default.ui.Controls.registerElement('captions', new TextSelection.Factory());
        loadSource();
        hideSpinner(container);
        // return () => {
        //     playerRef.current.destroy()
        //     uiRef.current.destroy()
        // }
    }, []);
    react_1.useEffect(function () {
        switch (action) {
            case 'play':
                videoRef.current.play();
                break;
            case 'pause':
                videoRef.current.pause();
                break;
            default:
        }
    }, [action]);
    var showControls = function () {
        if (!uiRef.current)
            return;
        var updatedControls = volumeSlider ? {
            controlPanelElements: withVolumeControl(const_1.defaultVideoConfig.controlPanelElements)
        } : {};
        uiRef.current.configure(__assign(__assign({}, const_1.defaultVideoConfig), updatedControls));
        videoRef.current.controls = false;
    };
    var handlePlaying = function (e) {
        e.stopPropagation();
        showControls();
        if (playView === 'fullscreen') {
            videoRef.current.requestFullscreen();
        }
        setPlaying(true);
        onPlay(e, { player: playerRef.current });
    };
    var handleOnPlayClick = function () {
        videoRef.current.play();
    };
    var handleVolumeChange = function (e) {
        var eventTarget = e.currentTarget;
        onVolumeChange(e, { volume: eventTarget.volume, muted: eventTarget.muted });
    };
    var handleOnPause = function () {
        // On IOS, the controls force showing up if the video exist fullscreen while playing.
        // This forces the controls to always hide
        videoRef.current.controls = false;
    };
    return (react_1.default.createElement("div", { style: { width: width + "px", height: height + "px" }, className: classnames_1.default('video-player', { 'video-player--poster': !playing }) },
        !playing && loaded && !failed && !buffering &&
            react_1.default.createElement("div", { className: "shaka-play-button-container" },
                react_1.default.createElement("button", { onClick: handleOnPlayClick, className: "shaka-play-button", style: { opacity: 1, zIndex: 999 }, "aria-label": a11yPlayText },
                    react_1.default.createElement(index_1.EbayIcon, { name: "videoPlay" }))),
        react_1.default.createElement("div", { className: "video-player__container", ref: containerRef },
            react_1.default.createElement("video", __assign({ ref: videoRef, style: { width: width + "px", height: height + "px" }, poster: thumbnail, muted: muted || false, onPlaying: handlePlaying, onPause: handleOnPause, onVolumeChange: handleVolumeChange }, rest), sources.map(function (source) {
                react_1.default.createElement("source", __assign({}, source));
            }))),
        react_1.default.createElement("div", { className: classnames_1.default('video-player__overlay', { 'video-player__overlay--hidden': !failed }) },
            react_1.default.createElement(index_1.EbayIcon, { name: "attention" }),
            react_1.default.createElement("div", { className: "video-player__overlay-text" }, errorText)),
        react_1.default.createElement("div", { className: classnames_1.default('video-player__overlay', {
                'video-player__overlay--hidden': loaded && (failed || !buffering)
            }) },
            react_1.default.createElement(index_1.EbayProgressSpinner, { size: "large", "aria-label": a11yLoadText }))));
};
function withVolumeControl(controls) {
    var insertAt = controls.length - 2 > 0 ? controls.length - 2 : controls.length;
    var controlsWithVolume = __spreadArrays(controls);
    controlsWithVolume.splice(insertAt, 0, 'volume');
    return controlsWithVolume;
}
function hideSpinner(container) {
    var shakaSpinner = container.querySelectorAll('.shaka-spinner')[0];
    if (shakaSpinner) {
        shakaSpinner.setAttribute('hidden', '');
    }
}
exports.default = EbayVideo;
