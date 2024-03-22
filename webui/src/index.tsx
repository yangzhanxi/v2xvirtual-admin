import React, {useEffect} from 'react';
import ReactDOM, {createRoot} from 'react-dom/client';
import {ConnectedRouter} from 'connected-react-router';
import {Provider} from 'react-redux';
import ReactModal from 'react-modal';
import {enableMapSet} from 'immer';

// import {init} from 'i18n/config';
import './dependencies';
import store, {runSaga} from './store/store';

import './index.css';
import history from 'store/history';

import {Routes} from './routes';

runSaga();

const App: React.FC = () => {
    // useEffect(() => {
    //     init(store.dispatch);
    // });
    return (
        <Provider store={store}>
            <ConnectedRouter history={history}>
                <Routes />
            </ConnectedRouter>
        </Provider>
    );
};

enableMapSet();

const appElement = document.getElementById('v2x-virtual-admin');

if (appElement) {
    ReactModal.setAppElement(appElement);
    const root = createRoot(appElement);
    root.render(<App />);
}
