import type { PartNum } from 'api/models/PartNumResponse';
import type {PortsApiResponse} from 'api/models/PortsResponse';

import {request as __request} from '../core/request';

export class NetworkControllerService {
    public static async getPorts(): Promise<PortsApiResponse> {
        const result = await __request({
            method: 'GET',
            path: `/ports`,
            errors: {
                401: `Invalid token or user not logged in`,
                422: `Invalid token or user not logged in`,
                403: `Invalid token or user not logged in`,
            },
        });

        return result.body;
    }

    public static async getPartNum(): Promise<PartNum> {
        const result = await __request({
            method: 'GET',
            path: `/partnum`,
            errors: {
                401: `Invalid token or user not logged in`,
                422: `Invalid token or user not logged in`,
                403: `Invalid token or user not logged in`,
            },
        });

        return result.body;
    }
}
