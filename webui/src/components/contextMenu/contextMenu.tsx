import {ContextMenu as OrionContextMenu, Placement} from 'orion-rwc';
import React from 'react';

export type ContextMenuItem = Readonly<{
    icon?: React.ReactNode;
    title: string;
    onSelect?: () => void;
    isHidden?: boolean;
    isDisabled?: boolean;
    tooltipText?: string;
    isLinkExternal?: boolean;
    link?: string;
}>;

export type ContextMenuProps = Readonly<{
    autoClose?: boolean;
    anchorNode: JSX.Element;
    isOpened: boolean;
    placement?: Placement;
    groups: readonly ContextMenuItem[][];
    isPinnedNodeSameMinWidth?: boolean;
    onClose: () => void;
}>;

const ContextMenu: React.FC<ContextMenuProps> = props => {
    const {groups} = props;
    return <OrionContextMenu itemGroups={groups} {...props} />;
};

ContextMenu.displayName = 'Cy-ContextMenu';

export default React.memo(ContextMenu);
