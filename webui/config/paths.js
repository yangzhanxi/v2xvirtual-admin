/* eslint-disable no-undef */
const path = require('path');

const root = path.resolve(__dirname, '../');

module.exports = {
    root,
    dist: path.resolve(root, 'dist'),
    appSrc: path.resolve(root, 'src'),
};
