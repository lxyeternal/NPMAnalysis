import { Injectable, Injector } from '@angular/core';
import { Overlay, OverlayConfig, OverlayContainer } from '@angular/cdk/overlay';
import { ComponentPortal, PortalInjector } from '@angular/cdk/portal';
import { ContextMenuComponent } from '../components/context-menu/context-menu.component';
import { ContextMenuConfig } from '../components/context-menu/context-menu-config';
import 'rxjs/add/operator/first';
var ContextMenuService = /** @class */ (function () {
    /**
     * @param {?} overlay
     * @param {?} parentInjector
     * @param {?} overlayContainer
     */
    function ContextMenuService(overlay, parentInjector, overlayContainer) {
        var _this = this;
        this.overlay = overlay;
        this.parentInjector = parentInjector;
        this.overlayContainer = overlayContainer;
        var overlayConfig = new OverlayConfig();
        overlayConfig.hasBackdrop = true;
        overlayConfig.positionStrategy = overlay.position().global().left('9999px').top('9999px');
        overlayConfig.backdropClass = 'cdk-overlay-transparent-backdrop';
        this.overlayRef = overlay.create(overlayConfig);
        this.overlayRef.backdropClick().subscribe(function () { return _this.detach(); });
    }
    /**
     *
     * @param {?} config
     * @return {?}
     */
    ContextMenuService.prototype.attach = function (config) {
        var _this = this;
        if (this.overlayRef.hasAttached()) {
            this.detach();
        }
        var /** @type {?} */ injector = this.createInjector(config), /** @type {?} */ // ContextMenuInjector(this.parentInjector, config),
        portal = new ComponentPortal(ContextMenuComponent, null, injector);
        var /** @type {?} */ componentRef = this.overlayRef.attach(portal);
        componentRef.instance.menuActionClick.first().subscribe(function () { return _this.detach(); });
        setTimeout(function () {
            var /** @type {?} */ overlayElement = _this.overlayRef.overlayElement, /** @type {?} */ overlayWidth = overlayElement.offsetWidth, /** @type {?} */ overlayHeight = overlayElement.offsetHeight, /** @type {?} */ containerElement = _this.overlayContainer.getContainerElement(), /** @type {?} */ containerWidth = containerElement.offsetWidth, /** @type {?} */ containerHeight = containerElement.offsetHeight, /** @type {?} */ left = config.left, /** @type {?} */ top = config.top;
            left = (left + overlayWidth > containerWidth) ? containerWidth - overlayWidth : left;
            top = (top + overlayHeight > containerHeight) ? containerHeight - overlayHeight : top;
            var /** @type {?} */ positionStrategy = (_this.overlayRef.getConfig().positionStrategy);
            positionStrategy.left(left + 'px').top(top + 'px');
            _this.overlayRef.updatePosition();
        }, 0);
    };
    /**
     * @return {?}
     */
    ContextMenuService.prototype.detach = function () {
        var /** @type {?} */ positionStrategy = (this.overlayRef.getConfig().positionStrategy);
        positionStrategy.left('9999px').top('9999px');
        this.overlayRef.updatePosition();
        this.overlayRef.detach(); // .then(() => console.log('ContextMenuComponent detached'));
    };
    /**
     * @param {?} config
     * @return {?}
     */
    ContextMenuService.prototype.createInjector = function (config) {
        // const userInjector = config && config.viewContainerRef && config.viewContainerRef.injector;
        var /** @type {?} */ injectionTokens = new WeakMap();
        injectionTokens.set(ContextMenuConfig, config);
        return new PortalInjector(/*userInjector || */ this.parentInjector, injectionTokens);
    };
    ContextMenuService.decorators = [
        { type: Injectable },
    ];
    /**
     * @nocollapse
     */
    ContextMenuService.ctorParameters = function () { return [
        { type: Overlay, },
        { type: Injector, },
        { type: OverlayContainer, },
    ]; };
    return ContextMenuService;
}());
export { ContextMenuService };
function ContextMenuService_tsickle_Closure_declarations() {
    /** @type {?} */
    ContextMenuService.decorators;
    /**
     * @nocollapse
     * @type {?}
     */
    ContextMenuService.ctorParameters;
    /** @type {?} */
    ContextMenuService.prototype.overlayRef;
    /** @type {?} */
    ContextMenuService.prototype.overlay;
    /** @type {?} */
    ContextMenuService.prototype.parentInjector;
    /** @type {?} */
    ContextMenuService.prototype.overlayContainer;
}
