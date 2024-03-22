import {all} from 'redux-saga/effects';

// import environmentSaga from 'domain/environment/environmentSaga';
// import scenariosPageSaga from 'pages/scenarios/scenariosPageSaga';
// import simulationHmiEventSseSaga from 'domain/simulation/simulationHmiEventSaga';
// import simulationInfoSaga from 'domain/simulation/simulationInfoSaga';
// import simulationSaga from 'domain/simulation/simulationSaga';
// import simulationSseSaga from 'domain/simulation/simulationSseSaga';
// import simulationVertexSseSaga from 'domain/simulation/simulationVertexEventSaga';
import licenseManagementSaga from 'domain/licenseManagement/licenseManagementSaga';

function getSagas() {
    console.log('11233');
    return [
        licenseManagementSaga(),
        // environmentSaga(),
        // simulationSaga(),
        // scenariosPageSaga(),
        // simulationInfoSaga(),
        // simulationSseSaga(),
        // simulationHmiEventSseSaga(),
        // simulationVertexSseSaga(),
    ];
}

export default function* rootSaga() {
    yield all(getSagas());
}
