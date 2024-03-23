import {FormProvider, useForm} from 'react-hook-form';
import {Button} from 'orion-rwc';
import React from 'react';
import {useHistory} from 'react-router';

import CommonPage from 'pages/common/commonPage';
import {AuthControllerService} from 'api/services/AuthControllerService';
import InputController from 'components/inputController/InputController';
import PasswordInputController from 'components/passwordInputCtl/PasswordInputController';
import routePaths from 'routePaths';
import {tokenUpdated} from 'domain/environment/environmentSlice';
import {useAppDispatch} from 'store/hooks';
import {useAsync} from 'utils/hooks';

import styles from './styles/authPage.scss';

const USERNAME = 'username';
const PASSWORD = 'password';

const AuthorizationPage: React.FC = () => {
    const formMethods = useForm<{[USERNAME]: string; [PASSWORD]: string}>({
        defaultValues: {
            [USERNAME]: '',
            [PASSWORD]: '',
        },
    });
    const {handleSubmit, watch} = formMethods;
    const dispatch = useAppDispatch();
    const username = watch(USERNAME, '');
    const password = watch(PASSWORD, '');
    const history = useHistory();
    const isSubmitButtonDisabled = !username || !password;
    const {exec, isPending, error} = useAsync(async () => {
        const response = await AuthControllerService.login({
            requestBody: {
                username,
                password,
            },
        });

        dispatch(tokenUpdated({token: response.access_token}));

        // wait for 1 second to update the store before redirecting (race condition)
        await new Promise(resolve => setTimeout(resolve, 1000));

        // if there is a query param with redirectTo, use it
        const redirectTo = new URLSearchParams(history.location.search).get('redirectTo');
        history.push(redirectTo ? redirectTo : routePaths.INDEX);
    });
    if (isPending) {
        console.log('loading');
    }
    if (error) {
        console.log('has error');
    }
    return (
        <CommonPage hideHeaderBar={true}>
            <div className={styles.root}>
                <span className={styles.icon}>V2X Virtual Admin</span>
                <FormProvider {...formMethods}>
                    <form onSubmit={handleSubmit(exec)}>
                        <div className={styles.authContainer}>
                            <div className={styles.title}>{'Sign in to V2X Virtual Admin'}</div>
                            <div className={styles.inputContainer}>
                                <InputController placeholder={'usename'} name={USERNAME} isInputRounded={true} />
                            </div>
                            <div className={styles.inputContainer}>
                                <PasswordInputController
                                    placeholder={'password'}
                                    name={PASSWORD}
                                    isInputRounded={true}
                                />
                            </div>
                            <Button
                                className={styles.submitButton}
                                text={'Login'}
                                isDisabled={isSubmitButtonDisabled}
                            />
                        </div>
                    </form>
                </FormProvider>
            </div>
        </CommonPage>
    );
};

export default React.memo(AuthorizationPage);
