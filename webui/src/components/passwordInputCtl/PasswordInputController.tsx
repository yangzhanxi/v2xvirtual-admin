import {Controller, useFormContext} from 'react-hook-form';
import React, {memo} from 'react';
import {PasswordInput} from 'orion-rwc';

const PasswordInputController: React.FC<{
    name: string;
    isInvalid?: boolean;
    placeholder?: string;
    isDisabled?: boolean;
    validationExpr?: RegExp;
    isInputRounded?: boolean;
    isPasswordInput?: boolean;
}> = props => {
    const {control} = useFormContext();

    const {name, isInvalid, placeholder, validationExpr, isDisabled} = props;

    return (
        <Controller
            name={name}
            render={({field: {onChange, onBlur, value, name: inputName, ref}}) => (
                <PasswordInput
                    isInputRounded={props.isInputRounded}
                    name={inputName}
                    value={value}
                    forwardedRef={ref}
                    placeholder={placeholder}
                    isInvalid={isInvalid}
                    isDisabled={isDisabled}
                    validationExpr={validationExpr}
                    onBlur={onBlur}
                    onValueChanged={onChange}
                />
            )}
            control={control}
        />
    );
};

export default memo(PasswordInputController);
