import React from 'react';
import classNames from 'classnames';

import styles from './styles/errorMessage.scss';

export enum TextSize {
    MEDIUM = 'MEDIUM',
    LARGE = 'LARGE',
}

const ErrorMessage: React.FC<{text?: string; textSize?: TextSize}> = ({text, textSize = TextSize.MEDIUM}) => {
    const errorText = text || 'Something went wrong';

    const className = classNames(styles.root, {
        [styles.mRootLarge]: textSize === TextSize.LARGE,
    });

    return <div className={className}>{errorText}</div>;
};

ErrorMessage.displayName = 'Cy-ErrorMessage';

export default React.memo(ErrorMessage);
