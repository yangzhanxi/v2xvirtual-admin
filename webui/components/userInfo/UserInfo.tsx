import React, {useState} from 'react';
import Image from 'next/image';

// import ContextMenu from '@/components/contextMenu/ContextMenu';
import {ContextMenu, ContextMenuItem, Placement} from 'orion-rwc';

import userIcon from '@/public/icons/logo.svg';
import expandedIcon from '@/public/icons/expanded.svg';

import styles from './styles/userInfo.module.scss';

const UserInfo: React.FC = () => {
    const [isOpenedMenu, setIsOpenedMenu] = useState(false);

    const button = (
        <div
            onClick={() => {
                setIsOpenedMenu(v => !v);
            }}>
            <Image className={styles.roundedIcon} alt='User' src={userIcon}/>
            <span> Admin User</span>
            <Image className={styles.collapsedIcon} alt='User' src={expandedIcon}/>
        </div>
    )
    const actions: ContextMenuItem[][] = [
        [{
            title: 'Logout',
            onSelect: () => {}
        }]
    ]
    const menu = (
        <ContextMenu
            anchorNode={button}
            isOpened={isOpenedMenu}
            itemGroups={actions}
            onClose={() => {
                setIsOpenedMenu(false);
            }}
        />
    )

    return <div>{menu}</div>
};

export default React.memo(UserInfo);