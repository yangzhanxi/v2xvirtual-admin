import {all} from 'redux-saga/effects';

import environmentSaga from 'domain/environment/environmentSaga';
import licenseManagementSaga from 'domain/licenseManagement/licenseManagementSaga';
import networkManagementSaga from 'domain/networkManagement/networkManagementSaga';

function getSagas() {
    return [licenseManagementSaga(), environmentSaga(), networkManagementSaga()];
}

export default function* rootSaga() {
    yield all(getSagas());
}
