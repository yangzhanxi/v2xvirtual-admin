// import environmentReducer from 'domain/environment/environmentSlice';
// import notificationsReducer from 'domain/notifications/notificationsSlice';
// import simulationReducers from 'domain/simulation/simulationReducers';

import {combineReducers} from 'redux';
import {History} from 'history';
import {connectRouter} from 'connected-react-router';

import licenseManagementReducer from 'domain/licenseManagement/licenseManagementSlice';
// import modalRendererReducer from 'components/modals/modalRenderer/modalRendererSlice';
// import scenariosPageReducer from 'pages/scenarios/scenariosPageSlice';

// import {stateReset} from 'store/globalActions';

// function resetWrapper<S, A extends AnyAction>(reducer: Reducer<S, A>): Reducer<S, A> {
//     return (state: S | undefined, action: A) => {
//         return reducer(action.type === stateReset.type ? undefined : state, action);
//     };
// }

export default (history: History) =>
    combineReducers({
        licenseManagement: licenseManagementReducer,
        // environment: environmentReducer,
        // modalRenderer: resetWrapper(modalRendererReducer),
        // notifications: resetWrapper(notificationsReducer),
        router: connectRouter(history),
        // scenariosPage: resetWrapper(scenariosPageReducer),
        // simulation: resetWrapper(simulationReducers),
    });
