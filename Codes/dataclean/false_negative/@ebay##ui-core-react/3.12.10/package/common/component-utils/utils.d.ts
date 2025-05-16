import { FC, ReactElement, ReactNode } from 'react';
import './array.polyfill.flat';
export declare function findComponent(nodes: ReactNode, componentType: FC): ReactElement | undefined;
export declare function excludeComponent(nodes: ReactNode, componentType: FC): ReactElement[];
export declare function filterByType(nodes: ReactNode, componentType: FC | FC[]): ReactElement[];
export declare function filterBy(nodes: ReactNode, predicate: (el: ReactElement) => boolean): ReactElement[];
//# sourceMappingURL=utils.d.ts.map