import {PayloadAction, createSlice} from '@reduxjs/toolkit/';

import {AuthControllerService} from 'api/services/AuthControllerService';
import RequestModel from 'api/models/RequestModel';
import {stateReset} from 'store/globalActions';

export const AccountDataRequest = new RequestModel({
    name: 'accountUser',
    request: AuthControllerService.currentuser,
});

type State = {
    language: string;
    isLoading: boolean;
    isInitialized: boolean;
    userData: {
        token: string;
        user: ReturnType<typeof AccountDataRequest.getDefaultState>;
    };
};

const DEFAULT_STATE: State = {
    language: '',
    isInitialized: false,
    isLoading: false,
    userData: {
        token: '',
        user: AccountDataRequest.getDefaultState(),
    },
};

const environmentSlice = createSlice({
    name: 'environment',
    initialState: DEFAULT_STATE,
    reducers: {
        isLoading(state, action: PayloadAction<boolean>) {
            const isLoading = action.payload;
            state.isLoading = isLoading;
        },
        isInitialized(state) {
            state.isInitialized = true;
        },
        tokenUpdated(state, action: PayloadAction<{token: string}>) {
            state.userData.token = action.payload.token;
        },
        languageLoaded(state, action: PayloadAction<{language: string}>) {
            const {language} = action.payload;
            state.language = language;
        },
    },
    extraReducers: builder => {
        builder.addCase(stateReset, state => {
            state.userData = DEFAULT_STATE.userData;
        });
        AccountDataRequest.addReducers(builder, state => state.userData.user);
    },
});

export const {isLoading, isInitialized, tokenUpdated, languageLoaded} = environmentSlice.actions;

export default environmentSlice.reducer;
