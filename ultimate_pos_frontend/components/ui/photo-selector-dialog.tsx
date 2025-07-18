"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { ProductImage } from "@/components/ui/product-image";
import { Photo, usePhotoOperations, usePhotos } from "@/lib/photo-hooks";
import {
  Check,
  Image as ImageIcon,
  Loader2,
  Trash2,
  Upload,
} from "lucide-react";
import { useEffect, useState } from "react";
import { toast } from "sonner";

interface PhotoSelectorDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  maxSelection?: number;
  preselectedIds?: number[];
  onSelectionChange: (selectedPhotos: Photo[]) => void;
  title?: string;
  description?: string;
}

export function PhotoSelectorDialog({
  open,
  onOpenChange,
  maxSelection = 5,
  preselectedIds = [],
  onSelectionChange,
  title = "Select Photos",
  description = "Choose photos from your gallery or upload new ones",
}: PhotoSelectorDialogProps) {
  const { photos, loading, setPhotos } = usePhotos();
  const {
    uploadPhoto,
    uploadMultiplePhotos,
    deletePhoto,
    uploading,
    deleting,
    uploadProgress,
  } = usePhotoOperations();
  const [selectedPhotos, setSelectedPhotos] = useState<Photo[]>([]);
  const [dragActive, setDragActive] = useState(false);

  // Set preselected photos when photos are loaded
  useEffect(() => {
    if (photos.length > 0 && preselectedIds.length > 0) {
      const preselected = photos.filter((photo) =>
        preselectedIds.includes(photo.id)
      );
      setSelectedPhotos(preselected);
    }
  }, [photos, preselectedIds]);

  const handlePhotoSelect = (photo: Photo) => {
    setSelectedPhotos((prev) => {
      const isSelected = prev.some((p) => p.id === photo.id);

      if (isSelected) {
        // Remove from selection
        return prev.filter((p) => p.id !== photo.id);
      } else {
        // Add to selection if under limit
        if (prev.length < maxSelection) {
          return [...prev, photo];
        } else {
          toast.error(`You can only select up to ${maxSelection} photos`);
          return prev;
        }
      }
    });
  };

  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    await handleFilesUpload(Array.from(files));

    // Reset the input
    event.target.value = "";
  };

  const handleFilesUpload = async (files: File[]) => {
    // Use the new uploadMultiplePhotos for better handling
    const uploadedPhotos = await uploadMultiplePhotos(files, {
      description: "Uploaded via photo selector",
      tags: ["gallery"],
    });

    if (uploadedPhotos.length > 0) {
      setPhotos((prev) => [...uploadedPhotos, ...prev]);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const droppedFiles = Array.from(e.dataTransfer.files).filter((file) =>
      file.type.startsWith("image/")
    );

    if (droppedFiles.length > 0) {
      await handleFilesUpload(droppedFiles);
    } else {
      toast.error("Please drop only image files");
    }
  };

  const handlePhotoDelete = async (photoId: number) => {
    if (
      !confirm(
        "Are you sure you want to delete this photo? This action cannot be undone."
      )
    ) {
      return;
    }

    const success = await deletePhoto(photoId);
    if (success) {
      setPhotos((prev) => prev.filter((p) => p.id !== photoId));
      setSelectedPhotos((prev) => prev.filter((p) => p.id !== photoId));
    }
  };

  const handleConfirm = () => {
    onSelectionChange(selectedPhotos);
    onOpenChange(false);
  };

  const handleCancel = () => {
    // Reset to preselected photos
    if (preselectedIds.length > 0) {
      const preselected = photos.filter((photo) =>
        preselectedIds.includes(photo.id)
      );
      setSelectedPhotos(preselected);
    } else {
      setSelectedPhotos([]);
    }
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[80vh] overflow-hidden flex flex-col">
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription>{description}</DialogDescription>
        </DialogHeader>

        {/* Upload Section */}
        <div
          className={`border-2 border-dashed rounded-lg p-4 mb-4 transition-colors ${
            dragActive
              ? "border-primary bg-primary/5"
              : "border-muted-foreground/25 hover:border-muted-foreground/50"
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="flex items-center justify-center">
            <label className="cursor-pointer">
              <input
                type="file"
                multiple
                accept="image/*"
                onChange={handleFileUpload}
                className="hidden"
                disabled={uploading}
              />
              <div className="flex items-center space-x-2 text-muted-foreground hover:text-foreground transition-colors">
                {uploading ? (
                  <Loader2 className="h-5 w-5 animate-spin" />
                ) : (
                  <Upload className="h-5 w-5" />
                )}
                <span>
                  {uploading
                    ? "Uploading..."
                    : dragActive
                    ? "Drop files here to upload"
                    : "Click to upload photos or drag and drop"}
                </span>
              </div>
            </label>
          </div>

          {/* Upload Progress */}
          {Object.keys(uploadProgress).length > 0 && (
            <div className="mt-4 space-y-2">
              {Object.entries(uploadProgress).map(([fileKey, progress]) => (
                <div key={fileKey} className="space-y-1">
                  <div className="flex justify-between text-xs text-muted-foreground">
                    <span>Uploading {fileKey.split("-")[0]}</span>
                    <span>{progress}%</span>
                  </div>
                  <div className="w-full bg-muted rounded-full h-1">
                    <div
                      className="bg-primary h-1 rounded-full transition-all duration-300"
                      style={{ width: `${progress}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          )}

          <p className="text-xs text-muted-foreground text-center mt-2">
            Supports: JPG, PNG, GIF, WebP (Max 5MB per file)
          </p>
        </div>

        {/* Selection Info */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <Badge variant="outline">
              {selectedPhotos.length} / {maxSelection} selected
            </Badge>
            {selectedPhotos.length > 0 && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setSelectedPhotos([])}
              >
                Clear selection
              </Button>
            )}
          </div>
        </div>

        {/* Photos Grid */}
        <div className="flex-1 overflow-y-auto">
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="h-8 w-8 animate-spin" />
              <span className="ml-2">Loading photos...</span>
            </div>
          ) : photos.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-8 text-muted-foreground">
              <ImageIcon className="h-12 w-12 mb-2" />
              <p>No photos found</p>
              <p className="text-sm">Upload some photos to get started</p>
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 pb-4">
              {photos.map((photo) => {
                const isSelected = selectedPhotos.some(
                  (p) => p.id === photo.id
                );

                return (
                  <div
                    key={photo.id}
                    className={`relative group cursor-pointer border-2 rounded-lg overflow-hidden transition-all ${
                      isSelected
                        ? "border-primary ring-2 ring-primary/20"
                        : "border-transparent hover:border-muted-foreground/50"
                    }`}
                    onClick={() => handlePhotoSelect(photo)}
                  >
                    <div className="aspect-square">
                      <ProductImage
                        src={photo.image}
                        alt={`Photo ${photo.id}`}
                        className="object-cover w-full h-full"
                      />
                    </div>

                    {/* Selection indicator */}
                    {isSelected && (
                      <div className="absolute top-2 left-2 bg-primary text-primary-foreground rounded-full p-1">
                        <Check className="h-3 w-3" />
                      </div>
                    )}

                    {/* Delete button */}
                    <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <Button
                        variant="destructive"
                        size="icon"
                        className="h-6 w-6"
                        onClick={(e) => {
                          e.stopPropagation();
                          handlePhotoDelete(photo.id);
                        }}
                        disabled={deleting}
                      >
                        {deleting ? (
                          <Loader2 className="h-3 w-3 animate-spin" />
                        ) : (
                          <Trash2 className="h-3 w-3" />
                        )}
                      </Button>
                    </div>

                    {/* Photo info overlay */}
                    <div className="absolute bottom-0 left-0 right-0 bg-black/50 text-white p-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <p className="text-xs truncate">ID: {photo.id}</p>
                      <p className="text-xs">
                        {new Date(photo.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        <DialogFooter className="border-t pt-4">
          <Button variant="outline" onClick={handleCancel}>
            Cancel
          </Button>
          <Button
            onClick={handleConfirm}
            disabled={selectedPhotos.length === 0}
          >
            Select {selectedPhotos.length} Photo
            {selectedPhotos.length !== 1 ? "s" : ""}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
