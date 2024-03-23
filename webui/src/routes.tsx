import {Redirect, Route, Switch} from 'react-router-dom';
import React from 'react';

import AuthorizationPage from 'pages/authorization/authPage';
import LicensesPage from 'pages/licenses/licensesPage';
import Protected from 'pages/protected/protected';

import routePaths from './routePaths';

const IndexRedirect = () => {
    const to = {
        pathname: routePaths.INDEX,
    };

    return <Redirect to={to} />;
};

export const Routes: React.FC = React.memo(() => {
    return (
        <Switch>
            <Route exact={true} path={routePaths.INDEX}>
                <Protected>
                    <LicensesPage />
                </Protected>
            </Route>
            <Route exact={true} path={routePaths.LICENSES}>
                <Protected>
                    <LicensesPage />
                </Protected>
            </Route>
            <Route exact={true} path={routePaths.AUTHORIZATION} component={AuthorizationPage} />

            {/*Fallback route*/}
            <Route component={IndexRedirect} />
        </Switch>
    );
});
