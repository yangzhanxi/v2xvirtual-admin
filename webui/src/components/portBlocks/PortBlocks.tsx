import React from 'react';

import PortBlock from 'components/portBlock/PortBlock';
import {PortsApiResponse} from 'api/models/PortsResponse';

import styles from './styles/portBlocks.scss';

const PortBlocks: React.FC<{
    ports: PortsApiResponse;
}> = ({ports}) => {
    const renderPorts = () => {
        return (
            <div className={styles.root}>
                {ports.map((p, index) => {
                    return <PortBlock port={p} key={index} />;
                })}
            </div>
        );
    };

    return renderPorts();
};

export default React.memo(PortBlocks);
