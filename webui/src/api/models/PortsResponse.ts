type PortAttributeData = {
    label: string,
    value: string
}

export type PortModel = {
    address: PortAttributeData,
    auto_negotiation: PortAttributeData,
    auto_negotiation_role: PortAttributeData,
    duplex_mode: PortAttributeData,
    gateway: PortAttributeData,
    ip_version: PortAttributeData,
    link_status: PortAttributeData,
    line_speed: PortAttributeData
    netmask: PortAttributeData,
    port_handel: PortAttributeData,
    port_name: PortAttributeData,
}

export type PortsApiResponse = PortModel[];
