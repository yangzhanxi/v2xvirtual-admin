import {RootState} from 'store/store';

export const isPortsSelector = (state: RootState) => {
    return state.networkManagement.ports;
};

export const isNetworkLoadingSelector = (state: RootState) => {
    return state.networkManagement.isLoading;
};

export const isPartNumSelector = (state: RootState) => {
    return state.networkManagement.partNum;
};
