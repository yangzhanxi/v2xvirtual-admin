import {call, fork, put, takeEvery} from '@redux-saga/core/effects';

import {getTokenFromLocalStorage, removeTokenFromLocalStorage, saveTokenToLocalStorage} from 'utils/auth';
import {OpenAPI} from 'api/core/OpenAPI';
import {stateReset} from 'store/globalActions';

import {AccountDataRequest, isInitialized, tokenUpdated} from './environmentSlice';

export default function* () {
    yield fork(AccountDataRequest.saga);
    yield takeEvery(stateReset, removeToken);
    yield takeEvery(tokenUpdated, updateToken);
    yield call(initializeEnvironment);
}

function removeToken() {
    OpenAPI.TOKEN = undefined;
    removeTokenFromLocalStorage();
}

function* initializeEnvironment() {
    const token = getTokenFromLocalStorage();

    if (token) {
        yield put(tokenUpdated({token}));
    }
    yield put(isInitialized());
}

function updateToken({payload}: ReturnType<typeof tokenUpdated>) {
    const {token} = payload;
    if (token) {
        OpenAPI.TOKEN = token;
        saveTokenToLocalStorage(token);
    }
}
