import {
    ActionReducerMapBuilder,
    PayloadAction,
    PayloadActionCreator,
    createAction,
    createReducer,
} from '@reduxjs/toolkit';
import {call, put, takeEvery} from 'redux-saga/effects';
import {Draft} from 'immer';
import {useCallback} from 'react';

import {useAppDispatch} from 'store/hooks';

interface RequestError {
    message: string;
}

interface State<R> {
    error?: RequestError;
    isLoading?: boolean;
    response?: R;
}

class RequestActionsModel<Params, Result> {
    readonly fulfilled: PayloadActionCreator<Result>;
    readonly pending: PayloadActionCreator<void>;
    readonly rejected: PayloadActionCreator<RequestError>;
    readonly requested: PayloadActionCreator<Params>;

    constructor(name: string) {
        const prefix = `api/${name}`;

        this.fulfilled = createAction<Result>(`${prefix}/fulfilled`);
        this.pending = createAction(`${prefix}/pending`) as PayloadActionCreator;
        this.rejected = createAction<RequestError>(`${prefix}/rejected`);
        this.requested = createAction<Params>(`${prefix}/requested`);
    }
}

class RequestModel<Result, Params = void> {
    readonly actions: RequestActionsModel<Params, Result>;
    readonly request: (params: Params) => Promise<Result>;

    constructor(args: {name: string; request: (params: Params) => Promise<Result>}) {
        this.actions = new RequestActionsModel<Params, Result>(args.name);
        this.request = args.request;
        this.executeRequest = this.executeRequest.bind(this);
        this.executeRequestSafe = this.executeRequestSafe.bind(this);
    }

    useRequest() {
        // eslint-disable-next-line react-hooks/rules-of-hooks
        const dispatch = useAppDispatch();
        // eslint-disable-next-line react-hooks/rules-of-hooks
        const request = useCallback(
            (params: Params) => {
                dispatch(this.actions.requested(params));
            },
            [dispatch]
        );
        return request;
    }

    public getPendingReducer<S>(reduceState: (sliceState: Draft<S>) => Draft<State<Result>>) {
        return (state: Draft<S>) => {
            const requestState = reduceState(state);

            requestState.isLoading = true;
            requestState.error = undefined;
        };
    }

    public getFulfilledReducer<S>(reduceState: (sliceState: Draft<S>) => Draft<State<Result>>) {
        return (state: Draft<S>, action: PayloadAction<any>) => {
            const requestState = reduceState(state);

            requestState.response = action.payload;
            requestState.isLoading = false;
            requestState.error = undefined;
        };
    }

    public getRejectedReducer<S>(reduceState: (sliceState: Draft<S>) => Draft<State<Result>>) {
        return (state: Draft<S>, action: PayloadAction<any>) => {
            const requestState = reduceState(state);

            requestState.error = action.payload;
            requestState.isLoading = false;
        };
    }

    public addPendingReducer<S>(
        builder: ActionReducerMapBuilder<S>,
        reduceState: (sliceState: Draft<S>) => Draft<State<Result>>
    ) {
        builder.addCase(this.actions.pending, this.getPendingReducer(reduceState));
    }

    public addFulfilledReducer<S>(
        builder: ActionReducerMapBuilder<S>,
        reduceState: (sliceState: Draft<S>) => Draft<State<Result>>
    ) {
        builder.addCase(this.actions.fulfilled, this.getFulfilledReducer(reduceState));
    }

    public addRejectedReducer<S>(
        builder: ActionReducerMapBuilder<S>,
        reduceState: (sliceState: Draft<S>) => Draft<State<Result>>
    ) {
        builder.addCase(this.actions.rejected, this.getRejectedReducer(reduceState));
    }

    public addReducers<S>(
        builder: ActionReducerMapBuilder<S>,
        reduceState: (sliceState: Draft<S>) => Draft<State<Result>>
    ) {
        this.addPendingReducer(builder, reduceState);
        this.addFulfilledReducer(builder, reduceState);
        this.addRejectedReducer(builder, reduceState);
    }

    public get reducer() {
        return createReducer<State<Result>>({} as State<Result>, builder => {
            this.addReducers<State<Result>>(builder, x => x);
        });
    }

    public *executeRequest(params: Params, throws = true) {
        try {
            yield put(this.actions.pending());

            const response: Result = yield call(this.request, params);

            yield put(this.actions.fulfilled(response));

            return response;
        } catch (e: any) {
            yield put(this.actions.rejected({message: e.body?.message || e?.message || ''}));

            if (throws) {
                throw e;
            }
        }
    }

    private *executeRequestSafe(action: PayloadAction<Params>) {
        yield this.executeRequest(action.payload, false);
    }

    public get saga() {
        // eslint-disable-next-line @typescript-eslint/no-this-alias
        const self = this;

        return function* executeRequestSaga() {
            yield takeEvery(self.actions.requested, self.executeRequestSafe);
        };
    }

    public getDefaultState(): State<Result> {
        return {
            error: undefined,
            isLoading: undefined,
            response: undefined,
        };
    }
}

export default RequestModel;
