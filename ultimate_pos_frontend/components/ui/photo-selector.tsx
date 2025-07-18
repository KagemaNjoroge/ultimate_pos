"use client";

import { Button } from "@/components/ui/button";
import { PhotoSelectorDialog } from "@/components/ui/photo-selector-dialog";
import { ProductImage } from "@/components/ui/product-image";
import { Photo } from "@/lib/photo-hooks";
import { Image as ImageIcon, X } from "lucide-react";
import { useState } from "react";

interface PhotoSelectorProps {
  selectedPhotos?: Photo[];
  onSelectionChange: (photos: Photo[]) => void;
  maxSelection?: number;
  buttonText?: string;
  buttonVariant?:
    | "default"
    | "outline"
    | "secondary"
    | "ghost"
    | "link"
    | "destructive";
  showPreviews?: boolean;
  className?: string;
}

export function PhotoSelector({
  selectedPhotos = [],
  onSelectionChange,
  maxSelection = 5,
  buttonText = "Select Photos",
  buttonVariant = "outline",
  showPreviews = true,
  className,
}: PhotoSelectorProps) {
  const [dialogOpen, setDialogOpen] = useState(false);

  const handleRemovePhoto = (photoId: number) => {
    const updated = selectedPhotos.filter((photo) => photo.id !== photoId);
    onSelectionChange(updated);
  };

  return (
    <div className={className}>
      {/* Trigger Button */}
      <Button
        variant={buttonVariant}
        onClick={() => setDialogOpen(true)}
        className="mb-4"
      >
        <ImageIcon className="mr-2 h-4 w-4" />
        {buttonText}
        {selectedPhotos.length > 0 && (
          <span className="ml-2 bg-primary/20 text-primary px-2 py-1 rounded-full text-xs">
            {selectedPhotos.length}
          </span>
        )}
      </Button>

      {/* Photo Previews */}
      {showPreviews && selectedPhotos.length > 0 && (
        <div className="space-y-2">
          <p className="text-sm font-medium">Selected Photos:</p>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2">
            {selectedPhotos.map((photo) => (
              <div key={photo.id} className="relative group">
                <div className="aspect-square border rounded-lg overflow-hidden">
                  <ProductImage
                    src={photo.image}
                    alt={`Selected photo ${photo.id}`}
                    className="object-cover w-full h-full"
                  />
                </div>
                <Button
                  variant="destructive"
                  size="icon"
                  className="absolute -top-2 -right-2 h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity"
                  onClick={() => handleRemovePhoto(photo.id)}
                >
                  <X className="h-3 w-3" />
                </Button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Photo Selector Dialog */}
      <PhotoSelectorDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        maxSelection={maxSelection}
        preselectedIds={selectedPhotos.map((p) => p.id)}
        onSelectionChange={onSelectionChange}
      />
    </div>
  );
}
