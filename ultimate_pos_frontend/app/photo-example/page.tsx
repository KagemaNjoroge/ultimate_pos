"use client";

import DashboardLayout from "@/components/layout/dashboard-layout";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { PhotoSelector } from "@/components/ui/photo-selector";
import { useFileUpload } from "@/lib/hooks";
import { Photo, usePhotoOperations } from "@/lib/photo-hooks";
import { Loader2, Upload } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

export default function PhotoExamplePage() {
  const [productName, setProductName] = useState("");
  const [selectedPhotos, setSelectedPhotos] = useState<Photo[]>([]);
  const [maxPhotos, setMaxPhotos] = useState(3);

  // For demonstrating direct multipart uploads
  const { uploadFile, uploading, uploadProgress } = useFileUpload();
  const { uploadPhoto, uploadMultiplePhotos } = usePhotoOperations();

  const handleDirectUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    for (const file of Array.from(files)) {
      try {
        await uploadFile(file, "/utils/photos/", {
          description: "Direct upload example",
          tags: ["example", "direct-upload"],
          category: "demo",
        });
      } catch (error) {
        console.error("Upload failed:", error);
      }
    }

    // Reset the input
    event.target.value = "";
  };

  const handleSave = () => {
    if (!productName.trim()) {
      toast.error("Please enter a product name");
      return;
    }

    const photoIds = selectedPhotos.map((p) => p.id);

    toast.success(
      `Product "${productName}" saved with ${
        photoIds.length
      } photos: [${photoIds.join(", ")}]`
    );

    console.log({
      productName,
      photoIds,
      selectedPhotos,
    });
  };

  const handleReset = () => {
    setProductName("");
    setSelectedPhotos([]);
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">
            Photo Selector Example
          </h2>
          <p className="text-muted-foreground">
            Demonstration of the photo selector component
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {/* Direct Multipart Upload Demo */}
          <Card>
            <CardHeader>
              <CardTitle>Direct Multipart Upload</CardTitle>
              <CardDescription>
                Upload files directly with progress tracking and metadata
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-4">
                <label className="cursor-pointer block">
                  <input
                    type="file"
                    multiple
                    accept="image/*"
                    onChange={handleDirectUpload}
                    className="hidden"
                    disabled={uploading}
                  />
                  <div className="flex flex-col items-center space-y-2 text-muted-foreground hover:text-foreground transition-colors">
                    {uploading ? (
                      <Loader2 className="h-8 w-8 animate-spin" />
                    ) : (
                      <Upload className="h-8 w-8" />
                    )}
                    <span className="text-sm text-center">
                      {uploading
                        ? "Uploading..."
                        : "Click to upload with metadata"}
                    </span>
                  </div>
                </label>
              </div>

              {/* Upload Progress */}
              {Object.keys(uploadProgress).length > 0 && (
                <div className="space-y-2">
                  <h4 className="text-sm font-medium">Upload Progress:</h4>
                  {Object.entries(uploadProgress).map(([fileKey, progress]) => (
                    <div key={fileKey} className="space-y-1">
                      <div className="flex justify-between text-xs">
                        <span className="truncate">
                          {fileKey.split("-")[0]}
                        </span>
                        <span>{progress}%</span>
                      </div>
                      <div className="w-full bg-muted rounded-full h-2">
                        <div
                          className="bg-primary h-2 rounded-full transition-all duration-300"
                          style={{ width: `${progress}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              )}

              <p className="text-xs text-muted-foreground">
                This demo shows direct multipart upload with custom metadata,
                progress tracking, and proper Content-Type headers.
              </p>
            </CardContent>
          </Card>

          {/* Example Form */}
          <Card>
            <CardHeader>
              <CardTitle>Product Form Example</CardTitle>
              <CardDescription>
                Create a product with photo selection
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="productName">Product Name</Label>
                <Input
                  id="productName"
                  placeholder="Enter product name"
                  value={productName}
                  onChange={(e) => setProductName(e.target.value)}
                />
              </div>

              <div>
                <Label htmlFor="maxPhotos">Max Photos Allowed</Label>
                <Input
                  id="maxPhotos"
                  type="number"
                  min="1"
                  max="10"
                  value={maxPhotos}
                  onChange={(e) => setMaxPhotos(Number(e.target.value))}
                />
              </div>

              <div>
                <Label>Product Photos</Label>
                <PhotoSelector
                  selectedPhotos={selectedPhotos}
                  onSelectionChange={setSelectedPhotos}
                  maxSelection={maxPhotos}
                  buttonText="Choose Product Photos"
                  showPreviews={true}
                />
              </div>

              <div className="flex space-x-2 pt-4">
                <Button onClick={handleSave} disabled={!productName.trim()}>
                  Save Product
                </Button>
                <Button variant="outline" onClick={handleReset}>
                  Reset
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Usage Information */}
          <Card>
            <CardHeader>
              <CardTitle>Component Features</CardTitle>
              <CardDescription>What this photo selector can do</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3 text-sm">
                <div>
                  <h4 className="font-medium">✅ Photo Selection</h4>
                  <p className="text-muted-foreground">
                    Select multiple photos from your gallery with configurable
                    limits
                  </p>
                </div>

                <div>
                  <h4 className="font-medium">✅ Photo Upload</h4>
                  <p className="text-muted-foreground">
                    Upload new photos directly from the dialog (5MB limit)
                  </p>
                </div>

                <div>
                  <h4 className="font-medium">✅ Photo Deletion</h4>
                  <p className="text-muted-foreground">
                    Delete photos from your gallery with confirmation
                  </p>
                </div>

                <div>
                  <h4 className="font-medium">✅ Preselection Support</h4>
                  <p className="text-muted-foreground">
                    Pass existing photo IDs to preselect them
                  </p>
                </div>

                <div>
                  <h4 className="font-medium">✅ Preview Thumbnails</h4>
                  <p className="text-muted-foreground">
                    Show selected photos with remove buttons
                  </p>
                </div>

                <div>
                  <h4 className="font-medium">✅ Loading States</h4>
                  <p className="text-muted-foreground">
                    Beautiful loading indicators for all operations
                  </p>
                </div>

                <div>
                  <h4 className="font-medium">✅ Error Handling</h4>
                  <p className="text-muted-foreground">
                    Comprehensive error handling with user feedback
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Usage Code Example */}
        <Card>
          <CardHeader>
            <CardTitle>Code Example</CardTitle>
            <CardDescription>
              How to use the PhotoSelector component
            </CardDescription>
          </CardHeader>
          <CardContent>
            <pre className="bg-muted p-4 rounded-lg overflow-x-auto text-sm">
              {`import { PhotoSelector } from "@/components/ui/photo-selector";
import { Photo } from "@/lib/photo-hooks";

function MyComponent() {
  const [selectedPhotos, setSelectedPhotos] = useState<Photo[]>([]);

  return (
    <PhotoSelector
      selectedPhotos={selectedPhotos}
      onSelectionChange={setSelectedPhotos}
      maxSelection={5}
      buttonText="Select Photos"
      showPreviews={true}
    />
  );
}`}
            </pre>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
