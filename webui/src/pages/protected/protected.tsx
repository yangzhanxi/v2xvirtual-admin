import React, {useEffect} from 'react';
import {SpinnerOverlay} from 'orion-rwc';

import {
    isEnvironmentInitializedSelector,
    isEnvironmentLoadingSelector,
    isUserLoadingSelector,
    userTokenSelector,
} from 'domain/environment/environmentSelector';
import {AccountDataRequest} from 'domain/environment/environmentSlice';
import routePaths from 'routePaths';
import {useAppSelector} from 'store/hooks';

import history from '../../store/history';

import styles from './styles/protected.scss';

type ProtectedProps = {
    children?: any;
};

const Protected = ({children}: ProtectedProps) => {
    const token = useAppSelector(userTokenSelector);
    const userAccountDataRequest = AccountDataRequest.useRequest();
    const isEnvironmentInitialized = useAppSelector(isEnvironmentInitializedSelector);
    const isEnvLoading = useAppSelector(isEnvironmentLoadingSelector);
    const isUserLoading = useAppSelector(isUserLoadingSelector);

    useEffect(() => {
        userAccountDataRequest();
    }, [userAccountDataRequest]);

    useEffect(() => {
        if (!token) {
            const prevLocation = `${history.location.pathname}${history.location.search}`;
            history.push(
                `${routePaths.AUTHORIZATION}${
                    prevLocation && prevLocation !== '/' ? `?redirectTo=${prevLocation}` : ''
                }`
            );
        }
    }, [token]);

    if (isEnvLoading === true || isUserLoading === true) {
        return (
            <div className={styles.root}>
                <SpinnerOverlay />
            </div>
        );
    }
    if (isEnvironmentInitialized) {
        return children;
    }
    return null;
};

export default Protected;
