import {FC, SVGProps} from 'react';

declare global {
    type SVGComponentType = FC<SVGProps<SVGElement>>;

    type ValueOf<T> = T[keyof T];
    type Optional<T, K extends keyof T> = Pick<Partial<T>, K> & Omit<T, K>;
    type Awaited<T> = T extends PromiseLike<infer U> ? Awaited<U> : T;
    type Resolved<T extends (...args: any[]) => any> = Awaited<ReturnType<T>>;
    type DeepPartial<T> = {[P in keyof T]?: DeepPartial<T[P]>};
}
