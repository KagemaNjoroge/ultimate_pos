import { api, apiService } from "@/lib/api";
import { useEffect, useState } from "react";
import { toast } from "sonner";

// Photo type definition based on your API response
export interface Photo {
  id: number;
  created_at: string;
  updated_at: string;
  image: string;
  image_url: string;
}

// Hook for managing photos
export function usePhotos() {
  const [photos, setPhotos] = useState<Photo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPhotos = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.photos.getAll();
      setPhotos(response.data || []);
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.message || err.message || "Failed to fetch photos";
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPhotos();
  }, []);

  return {
    photos,
    loading,
    error,
    refetch: fetchPhotos,
    setPhotos, // Allow manual updates
  };
}

// Hook for photo operations
export function usePhotoOperations() {
  const [uploading, setUploading] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [uploadProgress, setUploadProgress] = useState<{
    [key: string]: number;
  }>({});

  const uploadPhoto = async (
    file: File,
    metadata?: { description?: string; tags?: string[] }
  ): Promise<Photo | null> => {
    try {
      setUploading(true);

      // Validate file type
      if (!file.type.startsWith("image/")) {
        toast.error(`${file.name} is not a valid image file`);
        return null;
      }

      // Validate file size (5MB limit)
      if (file.size > 5 * 1024 * 1024) {
        toast.error(`${file.name} is too large. Please select files under 5MB`);
        return null;
      }

      // Create FormData for multipart upload
      const formData = new FormData();
      formData.append("image", file, file.name);

      // Add metadata if provided
      if (metadata?.description) {
        formData.append("description", metadata.description);
      }
      if (metadata?.tags && metadata.tags.length > 0) {
        formData.append("tags", JSON.stringify(metadata.tags));
      }

      // Add file metadata
      formData.append("file_name", file.name);
      formData.append("file_size", file.size.toString());
      formData.append("file_type", file.type);

      // Initialize progress tracking
      const fileKey = `${file.name}-${Date.now()}`;
      setUploadProgress((prev) => ({ ...prev, [fileKey]: 0 }));

      // Create axios config with progress tracking
      const config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (progressEvent: any) => {
          if (progressEvent.lengthComputable) {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setUploadProgress((prev) => ({
              ...prev,
              [fileKey]: percentCompleted,
            }));
          }
        },
      };

      // Upload using axios directly with progress tracking
      const response = await api.post("/utils/photos/", formData, config);

      // Clean up progress tracking
      setUploadProgress((prev) => {
        const newProgress = { ...prev };
        delete newProgress[fileKey];
        return newProgress;
      });

      toast.success(`${file.name} uploaded successfully`);
      return response.data;
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.message ||
        error.response?.data?.error ||
        error.message ||
        "Failed to upload photo";
      toast.error(errorMessage);
      return null;
    } finally {
      setUploading(false);
    }
  };

  const uploadMultiplePhotos = async (
    files: File[],
    metadata?: { description?: string; tags?: string[] }
  ): Promise<Photo[]> => {
    const results: Photo[] = [];

    for (const file of files) {
      const result = await uploadPhoto(file, metadata);
      if (result) {
        results.push(result);
      }
    }

    return results;
  };

  const deletePhoto = async (photoId: number): Promise<boolean> => {
    try {
      setDeleting(true);
      await apiService.photos.delete(photoId);
      toast.success("Photo deleted successfully");
      return true;
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.message ||
        error.message ||
        "Failed to delete photo";
      toast.error(errorMessage);
      return false;
    } finally {
      setDeleting(false);
    }
  };

  return {
    uploadPhoto,
    uploadMultiplePhotos,
    deletePhoto,
    uploading,
    deleting,
    uploadProgress,
  };
}
