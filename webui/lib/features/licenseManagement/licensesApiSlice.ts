import {createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

import { LicenseApiResponse } from "./licenseModels";

export const licensesApiSlice = createApi({
    baseQuery: fetchBaseQuery({baseUrl: 'http://localhost:5000/api/'}),
    reducerPath: 'licensesApi',
    tagTypes: ["Licenses"],
    endpoints: (build)=> ({
        getLicenses: build.query<LicenseApiResponse, void> ({
            query: () => 'licenses',
            providesTags: (result) => result ? result.map(({ name }) => ({ type: 'Licenses', name })) : [],
        })
    })
})

export const {useGetLicensesQuery} = licensesApiSlice;