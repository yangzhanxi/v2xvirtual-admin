import path from 'path'
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url)
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  distDir: 'dist',
  // sassOptions: {
  //   includePaths: [path.join(path.dirname(__filename), 'styles')]
  // }
};

export default nextConfig;
