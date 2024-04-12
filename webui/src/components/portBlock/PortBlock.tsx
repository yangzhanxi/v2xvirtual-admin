import React from 'react';

import LinkStatus from 'components/linkStatus/LinkStatus';
import PortAttribute from 'components/portAttribute/PortAttribute';
import {PortModel} from 'api/models/PortsResponse';

import styles from './styles/portBlock.scss';

const construtPortAttributeDatas = (port: PortModel) => {
    const port_attributes = [];
    port_attributes.push(<PortAttribute label={port.port_name.label} value={port.port_name.value} />);
    port_attributes.push(<LinkStatus label={port.link_status.label} value={port.link_status.value} />);
    port_attributes.push(<PortAttribute label={port.ip_version.label} value={port.ip_version.value} />);
    port_attributes.push(<PortAttribute label={port.address.label} value={port.address.value} />);
    port_attributes.push(<PortAttribute label={port.netmask.label} value={port.netmask.value} />);
    port_attributes.push(
        <PortAttribute
            label={port.auto_negotiation.label}
            value={port.auto_negotiation.value == 'true' ? 'Enable' : 'Disable'}
        />
    );
    port_attributes.push(
        <PortAttribute label={port.auto_negotiation_role.label} value={port.auto_negotiation_role.value} />
    );
    port_attributes.push(<PortAttribute label={port.duplex_mode.label} value={port.duplex_mode.value} />);
    port_attributes.push(<PortAttribute label={port.line_speed.label} value={port.line_speed.value} />);

    return port_attributes;
};

const PortBlock: React.FC<{port: PortModel}> = props => {
    const {port} = props;

    const port_attributes = construtPortAttributeDatas(port);
    const render_attributes = () =>
        port_attributes.map((a, index) => {
            return (
                <div className={styles.attribute} key={index}>
                    {a}
                </div>
            );
        });

    return <div className={styles.root}>{render_attributes()}</div>;
};

export default React.memo(PortBlock);
