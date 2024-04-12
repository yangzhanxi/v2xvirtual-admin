import {PayloadAction, createAction, createSlice} from '@reduxjs/toolkit';

import {License, LicenseApiResponse} from 'api/models/LicenseResponse';

type State = {
    licenses: LicenseApiResponse;
    isLoading: boolean;
};

const DEFAULT_STATE: State = {
    licenses: [],
    isLoading: false,
};

const licenseManagementSlice = createSlice({
    name: 'licenseManagement',
    initialState: DEFAULT_STATE,
    reducers: {
        isLoading(state, action: PayloadAction<boolean>) {
            const isLoading = action.payload;
            state.isLoading = isLoading;
        },
        updateLicenses(state, action: PayloadAction<{licenses: License[]}>) {
            const {licenses} = action.payload;
            state.licenses = licenses;
        },
    },
});

export const getLicensesRequested = createAction('GET_LICENSES_REQUESTED');

export const {updateLicenses, isLoading} = licenseManagementSlice.actions;

export default licenseManagementSlice.reducer;
