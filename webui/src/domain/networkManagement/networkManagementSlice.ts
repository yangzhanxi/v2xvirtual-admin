import {PayloadAction, createAction, createSlice} from '@reduxjs/toolkit';

import {PortModel, PortsApiResponse} from 'api/models/PortsResponse';
import {PartNum} from 'api/models/PartNumResponse';

type State = {
    ports: PortsApiResponse;
    partNum: string;
    isLoading: boolean;
};

const DEFAULT_STATE: State = {
    ports: [],
    partNum: '',
    isLoading: false,
};

const NetworkManagementSlice = createSlice({
    name: 'networkManagement',
    initialState: DEFAULT_STATE,
    reducers: {
        isLoading(state, action: PayloadAction<boolean>) {
            const isLoading = action.payload;
            state.isLoading = isLoading;
        },
        updatePorts(state, action: PayloadAction<{ports: PortModel[]}>) {
            const {ports} = action.payload;
            state.ports = ports;
        },
        updatePartNum(state, action: PayloadAction<{partNum: PartNum}>) {
            const {partNum} = action.payload;
            state.partNum = partNum.part_num;
        },
    },
});

export const getNetworkRequested = createAction('GET_NETWOKR_REQUESTED');

export const {updatePorts, updatePartNum, isLoading} = NetworkManagementSlice.actions;

export default NetworkManagementSlice.reducer;
