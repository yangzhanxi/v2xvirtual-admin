import { License } from "@/lib/features/licenseManagement/licenseModels"

export type LicenseRowItem = {
    id: string,
    index: number,
    name: string,
    start: string,
    expiration: string
}

export enum tableSortOption {
    ORDINAL_NUMBER = 'ordinal-number',
    SORT_BY_NAME = 'sortByName',
    SORT_BY_START = 'sortByStart',
    SORT_BY_EXPIRATION = 'sortByExpiration',
}

export function createLicenseRowItem(index:number, license: License): LicenseRowItem {
    return {
        id: license.name.toLocaleLowerCase().replace(' ', '-'),
        index,
        name: license.name,
        start: license.start,
        expiration: license.expiration
    }
}
