import type {AppDispatch} from './store';

//we created typed Dispatch for using it into sagas without cycle dependencies
const _internal = {
    dispatch: (() => {
        console.error('fake dispatch was called');
    }) as AppDispatch,
};

const appDispatch: AppDispatch = (...params) => _internal.dispatch(...params);

export {appDispatch, _internal};
