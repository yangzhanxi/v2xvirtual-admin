import React from 'react';

import HeaderButton from './HeaderButton';
import styles from './styles/headerBar.module.scss';

const HeaderBarItems: React.FC<{
    children?: React.ReactNode;
}> = ({children}) => {
    return (
        <div className={styles.headerPart}>
            {React.Children.map(children, (child, idx) => (
                <div key={idx} className={styles.eHeaderPartItem}>
                {child}
                </div>
            ))}
        </div>
    );
};

const HeaderBar: React.FC<{
    leftItems?: React.ReactNode;
    rightItems?: React.ReactNode;
}> = ({leftItems, rightItems}) => {
    return (
        <div className={styles.root} data-cy="header-bar">
            {leftItems || <HeaderBarItems />}
            {rightItems || <HeaderBarItems />}
        </div>
    );
};

HeaderBar.displayName = 'Cy-HeaderBar';

export default React.memo(HeaderBar);
export {HeaderBarItems, HeaderButton};
