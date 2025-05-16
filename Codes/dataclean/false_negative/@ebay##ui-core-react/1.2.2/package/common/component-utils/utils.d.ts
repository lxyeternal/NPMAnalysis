import { FC, ReactElement, ReactNode } from 'react';
export declare function findComponent(nodes: ReactNode, componentType: FC): ReactElement | undefined;
export declare function excludeComponent(nodes: ReactNode, componentType: FC): ReactElement[];
export declare function filterByType(nodes: ReactNode, componentType: FC, fn?: () => void): ReactElement[];
export declare function filterBy(nodes: ReactNode, predicate: (el: ReactElement) => boolean): ReactElement[];
//# sourceMappingURL=utils.d.ts.map