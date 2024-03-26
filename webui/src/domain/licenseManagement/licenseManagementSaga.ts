import {call, put, takeEvery} from 'redux-saga/effects';

import {LicnesesControllerService} from 'api/services/LicensesService';

import {getLicensesRequested, isLoading, updateLicenses} from './licenseManagementSlice';

export default function* () {
    yield takeEvery(getLicensesRequested, handleLicensesRequest);
}

function* handleLicensesRequest() {
    yield put(isLoading(true));

    try {
        const licenses: Resolved<typeof LicnesesControllerService.getLicenses> = yield call(() =>
            LicnesesControllerService.getLicenses()
        );

        yield put(updateLicenses({licenses: licenses}));
    } catch (e) {
        console.log(e);
    }
    yield put(isLoading(false));
}
