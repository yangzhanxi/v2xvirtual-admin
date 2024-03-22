import {MutableRefObject, useEffect, useRef, useState} from 'react';
import {debounce} from 'lodash';

export const useConstant = <T>(fn: () => T): T => {
    const ref = useRef<{val: T}>();

    if (!ref.current) {
        const val = fn();

        ref.current = {val};
    }

    return ref.current.val;
};

export const useIntersectionObserver = (
    ref: MutableRefObject<HTMLElement | null>,
    callback: IntersectionObserverCallback,
    options?: IntersectionObserverInit
) => {
    useEffect(() => {
        if (!ref.current) {
            return;
        }

        const observer = new IntersectionObserver(callback, options);

        observer.observe(ref.current);

        return () => observer.disconnect();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [callback, options]);
};

export const useAsync = <F extends (...args: any[]) => PromiseLike<any>>(callback: F) => {
    const [requestState, setRequestState] = useState<{
        data: Awaited<ReturnType<F>> | undefined;
        isPending: boolean;
        error: Error | null;
    }>({data: undefined, isPending: false, error: null});
    const runCounterRef = useRef(0);
    const savedCallback = useRef(callback);

    savedCallback.current = callback;

    useEffect(() => {
        return () => {
            // eslint-disable-next-line react-hooks/exhaustive-deps
            runCounterRef.current++;
        };
    }, []);

    const [exec] = useState(() => (...args: Parameters<F>) => {
        runCounterRef.current++;

        const currentRun = runCounterRef.current;

        setRequestState(rs => {
            return {...rs, isPending: true, error: null};
        });

        async function request() {
            try {
                const data = await savedCallback.current(...args);

                const isActual = currentRun === runCounterRef.current;

                if (isActual) {
                    setRequestState({data, isPending: false, error: null});
                }
            } catch (e) {
                const isActual = currentRun === runCounterRef.current;

                if (isActual) {
                    setRequestState(rs => {
                        return {...rs, isPending: false, error: e as Error};
                    });
                }
            }
        }

        request();
    });

    return {exec, ...requestState};
};

export function useInterval(callback: () => void, ms: number | null, firstCallImmediate = true) {
    const savedCallback = useRef(callback);

    savedCallback.current = callback;

    useEffect(() => {
        if (ms === null) {
            return;
        }

        const id = setInterval(() => savedCallback.current(), ms);

        return () => {
            clearInterval(id);
        };
    }, [ms]);

    useEffect(() => {
        if (ms === null) {
            return;
        }

        if (firstCallImmediate) {
            callback();
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);
}

export function useDebouncedValue<T>(val: T, ms: number): T {
    const [debouncedVal, setDebouncedVal] = useState(val);

    const [debouncedSet] = useState(() => debounce(setDebouncedVal, ms));

    useEffect(() => {
        debouncedSet(val);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [val]);

    useEffect(() => {
        return () => debouncedSet.cancel();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return debouncedVal;
}
