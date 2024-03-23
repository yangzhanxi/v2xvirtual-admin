import type {LicenseApiResponse} from 'api/models/LicenseResponse';

import {request as __request} from '../core/request';

export class LicnesesControllerService {
    public static async getLicenses(): Promise<LicenseApiResponse> {
        const result = await __request({
            method: 'GET',
            path: `/licenses`,
            errors: {
                401: `Invalid token or user not logged in`,
                422: `Invalid token or user not logged in`,
                403: `Invalid token or user not logged in`,
            },
        });

        return result.body;
    }
}
