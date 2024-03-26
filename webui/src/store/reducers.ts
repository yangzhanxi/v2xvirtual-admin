import {AnyAction, Reducer, combineReducers} from 'redux';
import {History} from 'history';
import {connectRouter} from 'connected-react-router';

import environmentReducer from 'domain/environment/environmentSlice';
import licenseManagementReducer from 'domain/licenseManagement/licenseManagementSlice';
import {stateReset} from 'store/globalActions';

function resetWrapper<S, A extends AnyAction>(reducer: Reducer<S, A>): Reducer<S, A> {
    return (state: S | undefined, action: A) => {
        return reducer(action.type === stateReset.type ? undefined : state, action);
    };
}

export default (history: History) =>
    combineReducers({
        environment: environmentReducer,
        licenseManagement: resetWrapper(licenseManagementReducer),
        router: connectRouter(history),
    });
