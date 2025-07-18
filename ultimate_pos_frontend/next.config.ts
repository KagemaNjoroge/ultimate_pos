import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "http",
        hostname: "localhost",
        port: "8000",
        pathname: "/media/**",
      },
      {
        protocol: "https",
        hostname: "localhost",
        port: "8000",
        pathname: "/media/**",
      },
      // Add your production domain when you deploy
      // {
      //   protocol: 'https',
      //   hostname: 'yourdomain.com',
      //   pathname: '/media/**',
      // },
    ],
  },
};

export default nextConfig;
