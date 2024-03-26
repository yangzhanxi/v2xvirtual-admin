import {getFromLocalStorage, removeFromLocalStorage, saveToLocalStorage} from 'domain/localStorage/storage';

const TOKEN_KEY = 'token';
const TOKEN_VERSION = 1;

export function saveTokenToLocalStorage(token: string) {
    saveToLocalStorage(TOKEN_KEY, TOKEN_VERSION, token);
}

export function removeTokenFromLocalStorage() {
    removeFromLocalStorage(TOKEN_KEY);
}

export function getTokenFromLocalStorage() {
    return getFromLocalStorage(TOKEN_KEY, TOKEN_VERSION);
}
