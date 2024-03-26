import React from 'react';
import classNames from 'classnames';

import styles from './styles/headerButton.scss';

const HeaderButton: React.FC<{
    Icon?: SVGComponentType;
    text?: string;
    isActive?: boolean;
    onClick?: () => void;
}> = ({Icon, text, isActive, onClick}) => {
    const iconStyle = classNames(styles.icon, {[styles.mIconWithText]: !!text});
    const icon = Icon && <Icon className={iconStyle} />;

    const rootClassName = classNames(styles.root, {
        [styles.mRootActive]: isActive,
    });

    return (
        <div className={rootClassName} onClick={onClick}>
            {icon}
            {text}
        </div>
    );
};

export default React.memo(HeaderButton);
