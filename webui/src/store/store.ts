import {configureStore} from '@reduxjs/toolkit';
import createSagaMiddleware from 'redux-saga';
import {routerMiddleware} from 'connected-react-router';

import history from 'store/history';

import rootSaga from '../saga/rootSaga';

import {_internal} from './utils';
import createRootReducer from './reducers';

const sagaMiddleware = createSagaMiddleware();

export const rootReducer = createRootReducer(history);

const store = configureStore({
    reducer: rootReducer,
    middleware: getDefaultMiddleware =>
        getDefaultMiddleware({thunk: false, serializableCheck: false})
            .concat(routerMiddleware(history))
            .concat(sagaMiddleware),
});

if (process.env.NODE_ENV !== 'production' && module.hot) {
    module.hot.accept('./reducers', () => store.replaceReducer(rootReducer));
}

_internal.dispatch = store.dispatch;

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

let sagaIsRunning = false;

export function runSaga() {
    console.log(111);
    if (sagaIsRunning) {
        console.error('saga already running');

        return;
    }

    sagaIsRunning = true;

    sagaMiddleware.run(rootSaga);
}

export default store;
