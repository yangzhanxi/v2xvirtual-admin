import {Dispatch} from 'redux';
import i18n from 'i18next';
import {initReactI18next} from 'react-i18next';

import {languageLoaded} from 'domain/environment/environmentSlice';

import common from './en/common.json';
import components from './en/components.json';
// import modals from './en/modals.json';
// import notifications from './en/notifications.json';
import pages from './en/pages.json';
// import validators from './en/validators.json';

export const resources = {
    en: {
        common,
        components,
        pages,
    },
} as const;

const ns = Object.keys(resources);

export const init = (dispatch: Dispatch) =>
    i18n.use(initReactI18next).init(
        {
            lng: 'en',
            ns,
            resources,
        },
        () => {
            if (dispatch) {
                dispatch(languageLoaded({language: i18n.language}));
            }
        }
    );
