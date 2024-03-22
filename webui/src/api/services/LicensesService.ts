import type {LicenseApiResponse} from 'api/models/LicenseResponse';

import {request as __request} from '../core/request';

export class LicnesesControllerService {
    public static async getLicenses(): Promise<LicenseApiResponse> {
        const result = await __request({
            method: 'GET',
            path: `/licenses`,
            errors: {
                500: `Error`,
            },
        });

        return result.body;
    }
}
