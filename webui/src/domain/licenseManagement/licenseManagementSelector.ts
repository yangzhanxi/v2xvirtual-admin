import {RootState} from 'store/store';

export const isLicensesSelector = (state: RootState) => {
    return state.licenseManagement.licenses;
};

export const isLicensesLoadingSelector = (state: RootState) => {
    return state.licenseManagement.isLoading;
};
