"use client";

import { Package } from "lucide-react";
import Image from "next/image";
import { useState } from "react";

interface ProductImageProps {
  src: string | null;
  alt: string;
  width?: number;
  height?: number;
  className?: string;
}

export function ProductImage({
  src,
  alt,
  width = 64,
  height = 64,
  className = "object-cover w-full h-full",
}: ProductImageProps) {
  const [imageError, setImageError] = useState(false);
  const [imageLoading, setImageLoading] = useState(true);

  if (!src || imageError) {
    return (
      <div className="flex items-center justify-center w-full h-full">
        <Package className="h-8 w-8 text-muted-foreground" />
      </div>
    );
  }

  return (
    <div className="relative w-full h-full">
      {imageLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-muted animate-pulse">
          <Package className="h-6 w-6 text-muted-foreground" />
        </div>
      )}
      <Image
        src={src}
        alt={alt}
        width={width}
        height={height}
        className={className}
        onLoad={() => setImageLoading(false)}
        onError={() => {
          setImageError(true);
          setImageLoading(false);
        }}
        unoptimized={
          process.env.NODE_ENV === "development" ||
          process.env.NEXT_PUBLIC_UNOPTIMIZED_IMAGES === "true"
        }
      />
    </div>
  );
}
