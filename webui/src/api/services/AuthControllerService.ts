import {AuthRequest, AuthResponse} from 'api/models/AuthModels';

import {request as __request} from '../core/request';

export class AuthControllerService {
    public static async logout(): Promise<any> {
        const result = await __request({
            method: 'POST',
            path: `/logout`,
            errors: {
                401: `Invalid token or user not logged in`,
            },
        });
        return result.body;
    }

    public static async login({requestBody}: {requestBody: AuthRequest}): Promise<AuthResponse> {
        const result = await __request({
            method: 'POST',
            path: `/login`,
            body: requestBody,
            errors: {
                401: `Invalid user or wrong password`,
                422: `Invalid user or wrong password`,
            },
        });
        return result.body;
    }

    public static async currentuser(): Promise<{username: string}> {
        const result = await __request({
            method: 'GET',
            path: `/currentuser`,
            errors: {
                401: `Invalid token or user not logged in`,
            },
        });
        return result.body;
    }
}
