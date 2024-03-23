interface LocalStorageValue<T> {
    version: number;
    value: T;
}

interface Storage {
    token: LocalStorageValue<string>;
}

export function getFromLocalStorage<K extends keyof Storage>(key: K, version: number): Storage[K]['value'] | undefined {
    if (!global.localStorage) {
        console.warn("Couldn't get access to local storage");
        return;
    }

    const rawVal = global.localStorage.getItem(key);

    if (!rawVal) {
        return;
    }

    try {
        const val: Storage[K] = JSON.parse(rawVal);
        if (val.version === version) {
            return val.value;
        } else if (val.version < version) {
            global.localStorage.removeItem(key);
        }
    } catch (e) {
        return;
    }
}

export function saveToLocalStorage<K extends keyof Storage>(key: K, version: number, value: Storage[K]['value']) {
    if (!global.localStorage) {
        console.warn("Couldn't get access to local storage");
        return;
    }

    try {
        const rawVal = JSON.stringify({
            value,
            version,
        } as LocalStorageValue<typeof value>);

        global.localStorage.setItem(key, rawVal);
    } catch (e) {
        // nothing to do
    }
}

export function removeFromLocalStorage<K extends keyof Storage>(key: K) {
    if (!global.localStorage) {
        console.warn("Couldn't get access to local storage");
        return;
    }

    global.localStorage.removeItem(key);
}
