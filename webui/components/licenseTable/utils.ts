import {Table} from 'orion-rwc'

import {License} from '@/lib/features/licenseManagement/licenseModels'
import { LicenseRowItem } from "./models";

export function sortByStartTime(a: LicenseRowItem, b: LicenseRowItem, sortOrder: Table.SortOrder) {
    const aVal = new Date(a.start).getTime();
    const bVal = new Date(b.start).getTime();

    if (sortOrder === Table.SortOrder.ASC) {
        return aVal > bVal ? 1 : -1;
    }
    return aVal > bVal ? -1 : 1;
}

export function sortByExpiration(a: LicenseRowItem, b: LicenseRowItem, sortOrder: Table.SortOrder) {
    const aVal = new Date(a.expiration).getTime();
    const bVal = new Date(b.expiration).getTime();

    if (sortOrder === Table.SortOrder.ASC) {
        return aVal > bVal ? 1 : -1;
    }
    return aVal > bVal ? -1 : 1;
}

export function sortByOrdinalNumber(a: LicenseRowItem, b: LicenseRowItem, sortOrder: Table.SortOrder) {
    const aVal = a.index;
    const bVal = b.index;

    if (sortOrder === Table.SortOrder.ASC) {
        return aVal > bVal ? 1 : -1;
    }
    return aVal > bVal ? -1 : 1;
}

export function sortByName(a: License | LicenseRowItem, b: License | LicenseRowItem, sortOrder: Table.SortOrder) {
    const aVal = a.name.toUpperCase()
    const bVal = b.name.toUpperCase()

    if (sortOrder === Table.SortOrder.ASC) {
        return aVal > bVal ? 1 : -1;
    }
    return aVal > bVal ? -1 : 1;
}

export function sortLicenses(a: License, b: License) {
    return sortByName(a, b, Table.SortOrder.ASC)
}
