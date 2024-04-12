import {call, put, takeEvery} from 'redux-saga/effects';

import {NetworkControllerService} from 'api/services/NetworkService';

import {getNetworkRequested, isLoading, updatePartNum, updatePorts} from './networkManagementSlice';

export default function* () {
    yield takeEvery(getNetworkRequested, handleNetworkRequest);
}

function* handleNetworkRequest() {
    yield put(isLoading(true));

    try {
        const partNum: Resolved<typeof NetworkControllerService.getPartNum> = yield call(() =>
            NetworkControllerService.getPartNum()
        );
        yield put(updatePartNum({partNum: partNum}));

        const ports: Resolved<typeof NetworkControllerService.getPorts> = yield call(() =>
            NetworkControllerService.getPorts()
        );
        yield put(updatePorts({ports: ports}));
    } catch (e) {
        console.log(e);
    }
    yield put(isLoading(false));
}
