import {Placement, SpinnerOverlay} from 'orion-rwc';
import React, {useState} from 'react';

import {ExpandedIcon, UserIcon} from 'assets/icons';
import {useAppDispatch, useAppSelector} from 'store/hooks';
import {AuthControllerService} from 'api/services/AuthControllerService';
import ContextMenu from 'components/contextMenu/contextMenu';
import {isUserSelector} from 'domain/environment/environmentSelector';
import {stateReset} from 'store/globalActions';
import {useAsync} from 'utils/hooks';

import styles from './styles/userInfo.scss';

const UserInfo: React.FC = () => {
    const dispatch = useAppDispatch();
    const {response: user} = useAppSelector(isUserSelector);
    const [isOpenedMenu, setIsOpenedMenu] = useState(false);
    const {exec, isPending} = useAsync(async () => {
        await AuthControllerService.logout();
        dispatch(stateReset());
    });

    const button = (
        <div
            className={styles.button}
            onClick={() => {
                setIsOpenedMenu(v => !v);
            }}>
            <UserIcon className={styles.roundedIcon} />
            <div className={styles.text} data-cy="user-info">{`${user?.username}`}</div>
            <ExpandedIcon className={styles.collapsedIcon} />
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
                        onSelect: exec,
                    },
                ],
            ]}
            onClose={() => {
                setIsOpenedMenu(false);
            }}
            placement={Placement.TOP_END}
        />
    );

    return isPending ? <SpinnerOverlay /> : <div className={styles.root}>{menu}</div>;
};

export default React.memo(UserInfo);
