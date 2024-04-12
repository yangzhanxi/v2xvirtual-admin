import React, {useEffect} from 'react';

import {
    isNetworkLoadingSelector,
    isPartNumSelector,
    isPortsSelector,
} from 'domain/networkManagement/networkManagementSelector';
import {useAppDispatch, useAppSelector} from 'store/hooks';
import CommonPage from 'pages/common/commonPage';
import PortBlocks from 'components/portBlocks/PortBlocks';
import Spinner from 'components/spinner/Spinner';
import V2xInfo from 'components/v2xInfo/V2xInfo';
import {getNetworkRequested} from 'domain/networkManagement/networkManagementSlice';

import styles from './styles/networkPage.scss';

const NetworkPage: React.FC = () => {
    const dispatch = useAppDispatch();
    useEffect(() => {
        dispatch(getNetworkRequested());
    }, [dispatch]);

    const partNum = useAppSelector(isPartNumSelector);
    const isLoading = useAppSelector(isNetworkLoadingSelector);
    const ports = useAppSelector(isPortsSelector);

    const renderNoPort = () => {
        return (
            <div className={styles.noPortContainer}>
                <div className={styles.noPortContext}>
                    <span> No ports found.</span>
                </div>
            </div>
        );
    };

    const renderContent = () => {
        if (isLoading) {
            return <Spinner />;
        }
        if (ports.length != 0) {
            return <PortBlocks ports={ports} />;
        }

        return renderNoPort();
    };

    return (
        <CommonPage>
            <V2xInfo partNum={partNum} />
            {renderContent()}
        </CommonPage>
    );
};

export default React.memo(NetworkPage);
