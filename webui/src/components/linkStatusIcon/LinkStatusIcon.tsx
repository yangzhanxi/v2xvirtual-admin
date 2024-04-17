import React from 'react';
import classNames from 'classnames';

import styles from './styles/linkStatusIcon.scss';

const LinkStatusIcon: React.FC<{
    linkStatus: string;
}> = ({linkStatus}) => {
    const linkStatusLowerCase = linkStatus.toLocaleLowerCase();

    const linkStatusClassName = classNames(styles.root, {
        [styles.mRootError]: linkStatusLowerCase === 'error',
        [styles.mRootAdminDown]: linkStatusLowerCase === 'down',
        [styles.mRootUp]: linkStatusLowerCase === 'up',
    });

    return <div className={linkStatusClassName} title={linkStatus} />;
};

export default React.memo(LinkStatusIcon);
