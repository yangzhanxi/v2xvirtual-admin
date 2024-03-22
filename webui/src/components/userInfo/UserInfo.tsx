import React, {useState} from 'react';
import Image from 'next/image';

import ContextMenu from '@/components/contextMenu/ContextMenu';
import userIcon from '@/public/icons/user.svg';
import expandedIcon from '@/public/icons/expanded.svg';
import styles from './styles/userInfo.scss';

const UserInfo: React.FC = () => {
    const [isOpenedMenu, setIsOpenedMenu] = useState(false);

    const button = (
        <div
            className={styles.button}
            onClick={() => {
                setIsOpenedMenu(v => !v);
            }}>
            {/* <Image className={styles.roundedIcon} alt='' src={userIcon}/> */}
            <span className={styles.text}> Admin User</span>
            {/* <Image className={styles.collapsedIcon} alt='' src={expandedIcon}/> */}
        </div>
    );

    const menu = (
        <ContextMenu
            anchorNode={button}
            isPinnedNodeSameMinWidth={true}
            isOpened={isOpenedMenu}
            autoClose={true}
            groups={[
                [
                    {
                        title: 'Logout',
                        onSelect: () => {},
                    },
                ],
            ]}
            onClose={() => {
                setIsOpenedMenu(false);
            }}
        />
    );

    return <div>{menu}</div>;
};

export default React.memo(UserInfo);
