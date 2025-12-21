import { ComponentProps, FC } from 'react';
import { FieldDescriptionType, FieldDescriptionPosition } from './types';
declare type DescriptionProps = ComponentProps<'div'> & ComponentProps<'span'> & {
    type?: FieldDescriptionType;
    position?: FieldDescriptionPosition;
};
declare const Description: FC<DescriptionProps>;
export default Description;
//# sourceMappingURL=description.d.ts.map