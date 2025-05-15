import { Injectable, Injector } from '@angular/core';
import { Overlay, OverlayConfig, OverlayContainer } from '@angular/cdk/overlay';
import { ComponentPortal, PortalInjector } from '@angular/cdk/portal';
import { ContextMenuComponent } from '../components/context-menu/context-menu.component';
import { ContextMenuConfig } from '../components/context-menu/context-menu-config';
import 'rxjs/add/operator/first';
export class ContextMenuService {
    /**
     * @param {?} overlay
     * @param {?} parentInjector
     * @param {?} overlayContainer
     */
    constructor(overlay, parentInjector, overlayContainer) {
        this.overlay = overlay;
        this.parentInjector = parentInjector;
        this.overlayContainer = overlayContainer;
        let overlayConfig = new OverlayConfig();
        overlayConfig.hasBackdrop = true;
        overlayConfig.positionStrategy = overlay.position().global().left('9999px').top('9999px');
        overlayConfig.backdropClass = 'cdk-overlay-transparent-backdrop';
        this.overlayRef = overlay.create(overlayConfig);
        this.overlayRef.backdropClick().subscribe(() => this.detach());
    }
    /**
     *
     * @param {?} config
     * @return {?}
     */
    attach(config) {
        if (this.overlayRef.hasAttached()) {
            this.detach();
        }
        let /** @type {?} */ injector = this.createInjector(config), /** @type {?} */ // ContextMenuInjector(this.parentInjector, config),
        portal = new ComponentPortal(ContextMenuComponent, null, injector);
        let /** @type {?} */ componentRef = this.overlayRef.attach(portal);
        componentRef.instance.menuActionClick.first().subscribe(() => this.detach());
        setTimeout(() => {
            let /** @type {?} */ overlayElement = this.overlayRef.overlayElement, /** @type {?} */ overlayWidth = overlayElement.offsetWidth, /** @type {?} */ overlayHeight = overlayElement.offsetHeight, /** @type {?} */ containerElement = this.overlayContainer.getContainerElement(), /** @type {?} */ containerWidth = containerElement.offsetWidth, /** @type {?} */ containerHeight = containerElement.offsetHeight, /** @type {?} */ left = config.left, /** @type {?} */ top = config.top;
            left = (left + overlayWidth > containerWidth) ? containerWidth - overlayWidth : left;
            top = (top + overlayHeight > containerHeight) ? containerHeight - overlayHeight : top;
            let /** @type {?} */ positionStrategy = (this.overlayRef.getConfig().positionStrategy);
            positionStrategy.left(left + 'px').top(top + 'px');
            this.overlayRef.updatePosition();
        }, 0);
    }
    /**
     * @return {?}
     */
    detach() {
        let /** @type {?} */ positionStrategy = (this.overlayRef.getConfig().positionStrategy);
        positionStrategy.left('9999px').top('9999px');
        this.overlayRef.updatePosition();
        this.overlayRef.detach(); // .then(() => console.log('ContextMenuComponent detached'));
    }
    /**
     * @param {?} config
     * @return {?}
     */
    createInjector(config) {
        // const userInjector = config && config.viewContainerRef && config.viewContainerRef.injector;
        const /** @type {?} */ injectionTokens = new WeakMap();
        injectionTokens.set(ContextMenuConfig, config);
        return new PortalInjector(/*userInjector || */ this.parentInjector, injectionTokens);
    }
}
ContextMenuService.decorators = [
    { type: Injectable },
];
/**
 * @nocollapse
 */
ContextMenuService.ctorParameters = () => [
    { type: Overlay, },
    { type: Injector, },
    { type: OverlayContainer, },
];
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
