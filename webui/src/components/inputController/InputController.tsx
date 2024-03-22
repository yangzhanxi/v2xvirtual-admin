import {Controller, useFormContext} from 'react-hook-form';
import {CounterInput, Input} from 'orion-rwc';
import React, {memo} from 'react';

const InputController: React.FC<{
    defaultValue?: string;
    maxLength?: number;
    name: string;
    isTextarea?: boolean;
    isInvalid?: boolean;
    placeholder?: string;
    isDisabled?: boolean;
    isHidden?: boolean;
    validationExpr?: RegExp;
    isInputRounded?: boolean;
    validator?: (value: string) => boolean | string;
}> = props => {
    const {control} = useFormContext();
    const {
        defaultValue,
        maxLength,
        name,
        isInputRounded,
        isTextarea,
        isInvalid,
        placeholder,
        validationExpr,
        isDisabled,
        isHidden,
        validator,
    } = props;

    const InputType = maxLength ? CounterInput : Input;

    return isHidden ? null : (
        <Controller
            name={name}
            rules={{validate: validator}}
            render={({field: {onChange, onBlur, value, name: inputName, ref}}) => (
                <>
                    <InputType
                        isInputRounded={isInputRounded}
                        name={inputName}
                        value={value}
                        forwardedRef={ref}
                        maxLength={maxLength!}
                        isTextarea={isTextarea}
                        placeholder={placeholder}
                        isInvalid={isInvalid}
                        isDisabled={isDisabled}
                        validationExpr={validationExpr}
                        onBlur={onBlur}
                        onValueChanged={onChange}
                    />
                </>
            )}
            control={control}
            defaultValue={defaultValue}
        />
    );
};

InputController.displayName = 'Cy-InputController';

export default memo(InputController);
