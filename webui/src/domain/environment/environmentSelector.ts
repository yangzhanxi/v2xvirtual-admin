import {RootState} from 'store/store';

export const userTokenSelector = (state: RootState) => state.environment.userData.token;

export const isEnvironmentInitializedSelector = (state: RootState) => state.environment.isInitialized;

export const isEnvironmentLoadingSelector = (state: RootState) => state.environment.isLoading;

export const isUserNameSelector = (state: RootState) => state.environment.userData.user;
