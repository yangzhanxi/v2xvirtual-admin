import {appDispatch} from 'store/utils';
import {stateReset} from 'store/globalActions';

import {ApiError} from './core/ApiError';

Object.defineProperty(ApiError.prototype, 'status', {
    set: function (status) {
        this._status = status;

        /* Handle Unauthorized error and reset state. API generator haven't any
        options to register custom listeners on errors.
        */
        if (status === 401) {
            appDispatch(stateReset());
        }
        if (status === 422) {
            appDispatch(stateReset());
        }
    },
    get: function () {
        return this._status;
    },
});
