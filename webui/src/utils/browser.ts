export const getBasePath = (isPathOnly?: boolean) => {
    const base: any = document.getElementById('v2x-admin-base');

    if (isPathOnly) {
        return base?.attributes.href.value;
    }

    return base?.href;
};
