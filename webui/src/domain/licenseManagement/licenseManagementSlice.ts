import {PayloadAction, createAction, createSlice} from '@reduxjs/toolkit';
// import {AuthControllerService, Parameters} from 'api/cv2x';
// import RequestModel from 'models/api/requestModel/RequestModel';

// import {stateReset} from 'store/globalActions';
import {License, LicenseApiResponse} from 'api/models/LicenseResponse';

// export const AccountDataRequest = new RequestModel({
//     name: 'accountUser',
//     request: AuthControllerService.currentuser,
// });

type State = {
    licenses: LicenseApiResponse;
    isLoading: boolean;
    // isLoading: boolean;
    // isInitialized: boolean;
    // userData: {
    //     token: string;
    //     accountData: ReturnType<typeof AccountDataRequest.getDefaultState>;
    // };
    // cachedData: {
    //     loginData: {aionServerUrl: string; email: string; checked: boolean | null};
    // };
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
        // isLoading(state, action: PayloadAction<boolean>) {
        //     const isLoading = action.payload;
        //     state.systemConfiguration.isLoaded = isLoading;
        // },

        // languageLoaded(state, action: PayloadAction<{language: string}>) {
        //     const {language} = action.payload;
        //     state.language = language;
        // },

        // updateMapView(state, action: PayloadAction<{isMapView: boolean}>) {
        //     const {isMapView} = action.payload;
        //     state.isMapView = isMapView;
        // },

        // systemConfigurationLoaded(state, action: PayloadAction<{isConfigured: boolean}>) {
        //     state.systemConfiguration.isLoaded = true;
        //     state.systemConfiguration.isConfigured = action.payload.isConfigured;
        //     state.systemConfiguration.error = null;
        // },
        // systemConfigurationLoadingFailed(state, action: PayloadAction<{error: string}>) {
        //     state.systemConfiguration.isLoaded = true;
        //     state.systemConfiguration.error = action.payload.error;
        // },
        // isInitialized(state) {
        //     state.isInitialized = true;
        // },
        // tokenUpdated(state, action: PayloadAction<{token: string}>) {
        //     state.userData.token = action.payload.token;
        // },
        // updateLoginData(state, action: PayloadAction<{aionServerUrl: string; email: string; checked: boolean}>) {
        //     state.cachedData.loginData.aionServerUrl = action.payload.aionServerUrl;
        //     state.cachedData.loginData.email = action.payload.email;
        //     state.cachedData.loginData.checked = action.payload.checked;
        // },

        // updateAllParams(state, action: PayloadAction<{allParams: Parameters}>) {
        //     state.allParams = action.payload.allParams;
        // },
    },
    // extraReducers: builder => {
    //     builder.addCase(stateReset, state => {
    //         // state.userData = DEFAULT_STATE.userData;
    //         // state.systemConfiguration = DEFAULT_STATE.systemConfiguration;
    //     });
    //     AccountDataRequest.addReducers(builder, state => state.userData.accountData);
    // },
});

// export const systemConfigCheckRequested = createAction('SYSTEM_CONFIG_CHECK_REQUESTED');
export const getLicensesRequested = createAction('GET_LICENSES_REQUESTED');

export const {updateLicenses, isLoading} = licenseManagementSlice.actions;

export default licenseManagementSlice.reducer;
